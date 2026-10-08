import express from "express";
import { randomBytes, randomUUID, scryptSync, timingSafeEqual } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { openDb, tx } from "./db.js";
import { confirmPayment, cancelPayment } from "./payments.js";
import * as C from "./config.js";

const { PRODUCTS, RULES, TZ } = C;
const HERE = dirname(fileURLToPath(import.meta.url));
const MIN = 60_000, HOUR = 60 * MIN, DAY = 24 * HOUR;

// ── 시간 도우미 (한국 시간 기준) ──
const kstDate = (d) => new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(d);
const kstIso = (dateStr, hour) => new Date(`${dateStr}T${String(hour).padStart(2, "0")}:00:00+09:00`).toISOString();
const kstLabel = (iso) => new Intl.DateTimeFormat("ko-KR", { timeZone: TZ, month: "long", day: "numeric", weekday: "short", hour: "numeric", minute: "2-digit" }).format(new Date(iso));

// ── 비밀번호 ──
function hashPw(pw) {
  const salt = randomBytes(16).toString("hex");
  return salt + ":" + scryptSync(pw, salt, 64).toString("hex");
}
function checkPw(pw, stored) {
  const [salt, hash] = stored.split(":");
  const a = Buffer.from(hash, "hex"), b = scryptSync(pw, salt, 64);
  return a.length === b.length && timingSafeEqual(a, b);
}
function safeEqual(a, b) {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && timingSafeEqual(x, y);
}

class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
const fail = (status, message) => { throw new HttpError(status, message); };

export function createApp({ dbPath = C.DB_PATH, now = () => Date.now() } = {}) {
  const db = openDb(dbPath);
  const app = express();
  app.disable("x-powered-by");
  app.set("trust proxy", 1);
  app.use(express.json({ limit: "32kb" }));

  // ── 실시간 연결 (Server-Sent Events) ──
  const roomStreams = new Map(); // bookingId → Set<res>
  const adminStreams = new Set();
  function openStream(req, res, set) {
    res.set({ "Content-Type": "text/event-stream", "Cache-Control": "no-cache", Connection: "keep-alive", "X-Accel-Buffering": "no" });
    res.flushHeaders();
    res.write("retry: 3000\n\n");
    set.add(res);
    const ping = setInterval(() => res.write(": ping\n\n"), 25_000);
    req.on("close", () => { clearInterval(ping); set.delete(res); });
  }
  function emit(set, event, data) {
    if (!set) return;
    const chunk = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
    for (const res of set) res.write(chunk);
  }

  function notify(text) {
    if (!C.TELEGRAM_BOT_TOKEN || !C.TELEGRAM_CHAT_ID) return;
    fetch(`https://api.telegram.org/bot${C.TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: C.TELEGRAM_CHAT_ID, text }),
    }).catch(() => {});
  }

  // ── 로그인 세션 ──
  const COOKIE = { user: "sid", admin: "admin_sid" };
  function readCookie(req, name) {
    const m = (req.headers.cookie || "").match(new RegExp(`(?:^|;\\s*)${name}=([^;]+)`));
    return m ? decodeURIComponent(m[1]) : null;
  }
  function setSession(res, { userId = null, admin = false }) {
    const token = randomBytes(32).toString("base64url");
    const days = admin ? 7 : 30;
    db.prepare("INSERT INTO auth_sessions (token, user_id, is_admin, expires_at) VALUES (?, ?, ?, ?)")
      .run(token, userId, admin ? 1 : 0, new Date(now() + days * DAY).toISOString());
    res.cookie(admin ? COOKIE.admin : COOKIE.user, token, {
      httpOnly: true, sameSite: "lax", secure: C.SECURE_COOKIES, maxAge: days * DAY, path: "/",
    });
  }
  function sessionFor(req, admin) {
    const token = readCookie(req, admin ? COOKIE.admin : COOKIE.user);
    if (!token) return null;
    const s = db.prepare("SELECT * FROM auth_sessions WHERE token = ?").get(token);
    if (!s || s.expires_at < new Date(now()).toISOString() || !!s.is_admin !== admin) return null;
    return s;
  }
  const requireUser = (req, _res, next) => {
    const s = sessionFor(req, false);
    if (!s) return next(new HttpError(401, "로그인이 필요합니다."));
    req.user = db.prepare("SELECT id, email, nickname FROM users WHERE id = ?").get(s.user_id);
    if (!req.user) return next(new HttpError(401, "로그인이 필요합니다."));
    next();
  };
  const requireAdmin = (req, _res, next) => (sessionFor(req, true) ? next() : next(new HttpError(401, "관리자 로그인이 필요합니다.")));

  // 무차별 로그인 시도 막기 (IP당 10분에 10번)
  const attempts = new Map();
  function throttle(req) {
    const key = req.ip, t = now();
    const a = attempts.get(key);
    if (!a || a.reset < t) { attempts.set(key, { count: 1, reset: t + 10 * MIN }); return; }
    if (++a.count > 10) fail(429, "시도가 너무 많습니다. 10분 뒤 다시 해 주세요.");
  }

  // ── 예약 도우미 ──
  function expireHolds() {
    db.prepare("UPDATE bookings SET status = 'expired' WHERE status = 'pending' AND created_at < ?")
      .run(new Date(now() - RULES.holdMinutes * MIN).toISOString());
  }
  function availableSlots() {
    expireHolds();
    const from = new Date(now() + RULES.bookAheadMinHours * HOUR).toISOString();
    const to = new Date(now() + RULES.bookAheadDays * DAY).toISOString();
    return db.prepare(`
      SELECT s.starts_at FROM slots s
      WHERE s.starts_at >= ? AND s.starts_at <= ?
        AND NOT EXISTS (SELECT 1 FROM bookings b WHERE b.starts_at = s.starts_at AND b.status IN ('pending','paid','done','noshow'))
      ORDER BY s.starts_at`).all(from, to).map((r) => r.starts_at);
  }
  function roomPhase(b) {
    const t = now(), start = Date.parse(b.starts_at), end = Date.parse(b.ends_at);
    if (b.status !== "paid") return "closed";
    if (t < start - RULES.enterBeforeMin * MIN) return "waiting";
    if (t <= end) return "open";
    return "ended";
  }
  function publicBooking(b, extra = {}) {
    return {
      id: b.id, product: b.product, productName: PRODUCTS[b.product]?.name ?? b.product, amount: b.amount,
      startsAt: b.starts_at, endsAt: b.ends_at, status: b.status, phase: roomPhase(b),
      intake: b.intake, createdAt: b.created_at, paidAt: b.paid_at, canceledAt: b.canceled_at,
      cancelReason: b.cancel_reason, refundedAmount: b.refunded_amount,
      canCancel: b.status === "paid" && Date.parse(b.starts_at) - now() >= RULES.freeCancelHours * HOUR,
      ...extra,
    };
  }
  function addMessage(bookingId, sender, body) {
    const createdAt = new Date(now()).toISOString();
    const { lastInsertRowid } = db.prepare("INSERT INTO messages (booking_id, sender, body, created_at) VALUES (?, ?, ?, ?)")
      .run(bookingId, sender, body, createdAt);
    const msg = { id: Number(lastInsertRowid), sender, body, createdAt };
    emit(roomStreams.get(bookingId), "message", msg);
    emit(adminStreams, "message", { bookingId, ...msg });
    return msg;
  }
  const listMessages = (bookingId) =>
    db.prepare("SELECT id, sender, body, created_at AS createdAt FROM messages WHERE booking_id = ? ORDER BY id").all(bookingId);

  const ah = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

  // ═════════════ 고객 API ═════════════
  app.get("/api/config", (_req, res) => {
    res.json({
      products: Object.entries(PRODUCTS).map(([id, p]) => ({ id, ...p })),
      rules: { enterBeforeMin: RULES.enterBeforeMin, freeCancelHours: RULES.freeCancelHours },
      paymentMode: C.PAYMENT_MODE,
      tossClientKey: C.PAYMENT_MODE === "toss" ? C.TOSS_CLIENT_KEY : null,
    });
  });

  app.post("/api/signup", (req, res) => {
    throttle(req);
    const email = String(req.body.email || "").trim().toLowerCase();
    const password = String(req.body.password || "");
    const nickname = String(req.body.nickname || "").trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) fail(400, "이메일 형식을 확인해 주세요.");
    if (password.length < 8) fail(400, "비밀번호는 8자 이상으로 정해 주세요.");
    if (!nickname || nickname.length > 20) fail(400, "닉네임은 1~20자로 정해 주세요.");
    if (db.prepare("SELECT 1 FROM users WHERE email = ?").get(email)) fail(409, "이미 가입된 이메일입니다. 로그인해 주세요.");
    const id = randomUUID();
    db.prepare("INSERT INTO users (id, email, pw_hash, nickname, created_at) VALUES (?, ?, ?, ?, ?)")
      .run(id, email, hashPw(password), nickname, new Date(now()).toISOString());
    setSession(res, { userId: id });
    res.json({ user: { id, email, nickname } });
  });

  app.post("/api/login", (req, res) => {
    throttle(req);
    const email = String(req.body.email || "").trim().toLowerCase();
    const u = db.prepare("SELECT * FROM users WHERE email = ?").get(email);
    if (!u || !checkPw(String(req.body.password || ""), u.pw_hash)) fail(401, "이메일 또는 비밀번호가 맞지 않습니다.");
    setSession(res, { userId: u.id });
    res.json({ user: { id: u.id, email: u.email, nickname: u.nickname } });
  });

  app.post("/api/logout", (req, res) => {
    const token = readCookie(req, COOKIE.user);
    if (token) db.prepare("DELETE FROM auth_sessions WHERE token = ?").run(token);
    res.clearCookie(COOKIE.user, { path: "/" });
    res.json({ ok: true });
  });

  app.get("/api/me", (req, res) => {
    const s = sessionFor(req, false);
    const user = s && db.prepare("SELECT id, email, nickname FROM users WHERE id = ?").get(s.user_id);
    res.json({ user: user || null });
  });

  app.get("/api/slots", (_req, res) => res.json({ slots: availableSlots() }));

  // 예약 만들기 (결제 전 임시 예약)
  app.post("/api/bookings", requireUser, (req, res) => {
    const { product, startsAt, intake, agreeTerms, agreeSensitive, agreeCrisis } = req.body;
    const p = PRODUCTS[product];
    if (!p) fail(400, "상품을 골라 주세요.");
    if (!agreeTerms || !agreeSensitive || !agreeCrisis) fail(400, "필수 동의 항목을 확인해 주세요.");
    const text = String(intake || "").trim();
    if (text.length < 10) fail(400, "상담 전에 상황을 10자 이상 적어 주세요.");
    if (text.length > 3000) fail(400, "사연은 3000자 안으로 줄여 주세요.");
    if (!availableSlots().includes(startsAt)) fail(409, "그 시간은 방금 마감됐습니다. 다른 시간을 골라 주세요.");

    const id = randomUUID();
    const orderId = "ord_" + randomBytes(12).toString("hex");
    const endsAt = new Date(Date.parse(startsAt) + p.minutes * MIN).toISOString();
    try {
      db.prepare(`INSERT INTO bookings (id, order_id, user_id, product, amount, starts_at, ends_at, intake, status, created_at)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)`)
        .run(id, orderId, req.user.id, product, p.price, startsAt, endsAt, text, new Date(now()).toISOString());
    } catch {
      fail(409, "그 시간은 방금 마감됐습니다. 다른 시간을 골라 주세요.");
    }
    res.json({
      bookingId: id, orderId, amount: p.price,
      orderName: `${p.name} · ${kstLabel(startsAt)}`,
      customerKey: "cus_" + req.user.id.replace(/-/g, ""),
      customerName: req.user.nickname, customerEmail: req.user.email,
    });
  });

  // 결제 승인 (결제창에서 돌아온 뒤 호출)
  app.post("/api/payments/confirm", requireUser, ah(async (req, res) => {
    const paymentKey = String(req.body.paymentKey || "");
    const orderId = String(req.body.orderId || "");
    const amount = Number(req.body.amount);
    const b = db.prepare("SELECT * FROM bookings WHERE order_id = ? AND user_id = ?").get(orderId, req.user.id);
    if (!b) fail(404, "주문을 찾을 수 없습니다.");
    if (b.status === "paid" && b.payment_key === paymentKey) return res.json({ booking: publicBooking(b) });
    if (amount !== b.amount) fail(400, "결제 금액이 주문과 다릅니다.");
    if (!["pending", "expired"].includes(b.status)) fail(409, "이미 처리된 주문입니다.");
    if (b.status === "expired") {
      // 결제창에 오래 머문 경우: 그사이 시간이 안 잡혔으면 다시 잡아둠
      try { db.prepare("UPDATE bookings SET status = 'pending', created_at = ? WHERE id = ?").run(new Date(now()).toISOString(), b.id); }
      catch { fail(409, "결제하시는 동안 그 시간이 마감됐습니다. 결제는 승인되지 않았으니 다른 시간을 골라 주세요."); }
    }

    try {
      await confirmPayment({ paymentKey, orderId, amount });
    } catch (e) {
      fail(402, `결제가 승인되지 않았습니다: ${e.message}`);
    }
    db.prepare("UPDATE bookings SET status = 'paid', payment_key = ?, paid_at = ? WHERE id = ?")
      .run(paymentKey, new Date(now()).toISOString(), b.id);
    const paid = db.prepare("SELECT * FROM bookings WHERE id = ?").get(b.id);
    addMessage(b.id, "system", `예약이 확정됐습니다. ${kstLabel(b.starts_at)}에 시작합니다. 시작 ${RULES.enterBeforeMin}분 전부터 이 방에서 기다려 주세요.`);
    emit(adminStreams, "booking", publicBooking(paid, { nickname: req.user.nickname }));
    notify(`🗓 새 상담 예약\n${req.user.nickname} · ${PRODUCTS[b.product]?.name}\n${kstLabel(b.starts_at)}\n\n${b.intake.slice(0, 300)}`);
    res.json({ booking: publicBooking(paid) });
  }));

  app.get("/api/bookings", requireUser, (req, res) => {
    const rows = db.prepare("SELECT * FROM bookings WHERE user_id = ? AND status NOT IN ('pending','expired') ORDER BY starts_at DESC").all(req.user.id);
    res.json({ bookings: rows.map((b) => publicBooking(b)) });
  });

  function userBooking(req) {
    const b = db.prepare("SELECT * FROM bookings WHERE id = ? AND user_id = ?").get(req.params.id, req.user.id);
    if (!b) fail(404, "상담을 찾을 수 없습니다.");
    return b;
  }

  app.get("/api/bookings/:id", requireUser, (req, res) => {
    const b = userBooking(req);
    res.json({ booking: publicBooking(b), messages: listMessages(b.id), serverNow: new Date(now()).toISOString() });
  });

  app.get("/api/bookings/:id/stream", requireUser, (req, res) => {
    const b = userBooking(req);
    if (!roomStreams.has(b.id)) roomStreams.set(b.id, new Set());
    openStream(req, res, roomStreams.get(b.id));
  });

  app.post("/api/bookings/:id/messages", requireUser, (req, res) => {
    const b = userBooking(req);
    const body = String(req.body.body || "").trim();
    if (!body) fail(400, "내용을 입력해 주세요.");
    if (body.length > 2000) fail(400, "한 번에 2000자까지 보낼 수 있습니다.");
    const phase = roomPhase(b);
    if (phase === "waiting") fail(403, `상담 시작 ${RULES.enterBeforeMin}분 전부터 보낼 수 있습니다.`);
    if (phase !== "open") fail(403, "상담 시간이 끝났습니다.");
    const msg = addMessage(b.id, "user", body);
    res.json({ message: msg });
  });

  app.post("/api/bookings/:id/cancel", requireUser, ah(async (req, res) => {
    const b = userBooking(req);
    if (!publicBooking(b).canCancel) fail(403, `시작 ${RULES.freeCancelHours}시간 전까지만 직접 취소할 수 있습니다. 사정이 있으면 채팅방에 남겨 주세요.`);
    await refund(b, "고객 취소", b.amount);
    notify(`↩️ 예약 취소 (고객)\n${req.user.nickname} · ${kstLabel(b.starts_at)}`);
    res.json({ booking: publicBooking(db.prepare("SELECT * FROM bookings WHERE id = ?").get(b.id)) });
  }));

  async function refund(b, reason, amount) {
    try {
      await cancelPayment({ paymentKey: b.payment_key, reason, amount: amount < b.amount ? amount : undefined, idempotencyKey: `cancel-${b.id}` });
    } catch (e) {
      fail(502, `환불 처리에 실패했습니다: ${e.message}`);
    }
    db.prepare("UPDATE bookings SET status = 'canceled', canceled_at = ?, cancel_reason = ?, refunded_amount = ? WHERE id = ?")
      .run(new Date(now()).toISOString(), reason, amount, b.id);
    addMessage(b.id, "system", `예약이 취소됐습니다. ${amount.toLocaleString("ko-KR")}원이 환불 처리됩니다.`);
    emit(adminStreams, "booking", { id: b.id, status: "canceled" });
  }

  // ═════════════ 관리자 API ═════════════
  app.post("/api/admin/login", (req, res) => {
    throttle(req);
    if (!C.ADMIN_PASSWORD) fail(503, "서버에 ADMIN_PASSWORD가 설정되지 않았습니다.");
    if (!safeEqual(req.body.password || "", C.ADMIN_PASSWORD)) fail(401, "비밀번호가 맞지 않습니다.");
    setSession(res, { admin: true });
    res.json({ ok: true });
  });
  app.post("/api/admin/logout", (req, res) => {
    const token = readCookie(req, COOKIE.admin);
    if (token) db.prepare("DELETE FROM auth_sessions WHERE token = ?").run(token);
    res.clearCookie(COOKIE.admin, { path: "/" });
    res.json({ ok: true });
  });
  app.get("/api/admin/me", (req, res) => res.json({ admin: !!sessionFor(req, true) }));

  app.get("/api/admin/stream", requireAdmin, (req, res) => openStream(req, res, adminStreams));

  app.get("/api/admin/bookings", requireAdmin, (req, res) => {
    expireHolds();
    const past = req.query.scope === "past";
    const cutoff = new Date(now() - 2 * HOUR).toISOString();
    const rows = db.prepare(`
      SELECT b.*, u.nickname, u.email,
        (SELECT COUNT(*) FROM messages m WHERE m.booking_id = b.id AND m.sender = 'user') AS user_msgs
      FROM bookings b JOIN users u ON u.id = b.user_id
      WHERE b.status NOT IN ('pending','expired') AND ${past ? "b.ends_at < ?" : "b.ends_at >= ?"}
      ORDER BY b.starts_at ${past ? "DESC LIMIT 200" : "ASC"}`).all(cutoff);
    res.json({ bookings: rows.map((b) => publicBooking(b, { nickname: b.nickname, email: b.email, userMessages: b.user_msgs })) });
  });

  function adminBooking(req) {
    const b = db.prepare("SELECT b.*, u.nickname, u.email FROM bookings b JOIN users u ON u.id = b.user_id WHERE b.id = ?").get(req.params.id);
    if (!b) fail(404, "상담을 찾을 수 없습니다.");
    return b;
  }

  app.get("/api/admin/bookings/:id", requireAdmin, (req, res) => {
    const b = adminBooking(req);
    const history = db.prepare(`SELECT id, product, starts_at AS startsAt, status FROM bookings
      WHERE user_id = ? AND id != ? AND status IN ('paid','done','noshow') ORDER BY starts_at DESC`).all(b.user_id, b.id);
    res.json({ booking: publicBooking(b, { nickname: b.nickname, email: b.email, history }), messages: listMessages(b.id), serverNow: new Date(now()).toISOString() });
  });

  app.get("/api/admin/bookings/:id/stream", requireAdmin, (req, res) => {
    const b = adminBooking(req);
    if (!roomStreams.has(b.id)) roomStreams.set(b.id, new Set());
    openStream(req, res, roomStreams.get(b.id));
  });

  app.post("/api/admin/bookings/:id/messages", requireAdmin, (req, res) => {
    const b = adminBooking(req);
    const body = String(req.body.body || "").trim();
    if (!body) fail(400, "내용을 입력해 주세요.");
    if (body.length > 4000) fail(400, "한 번에 4000자까지 보낼 수 있습니다.");
    if (b.status !== "paid") fail(403, "종료되거나 취소된 상담입니다.");
    res.json({ message: addMessage(b.id, "admin", body) });
  });

  app.post("/api/admin/bookings/:id/status", requireAdmin, (req, res) => {
    const b = adminBooking(req);
    const status = req.body.status;
    if (!["done", "noshow", "paid"].includes(status)) fail(400, "알 수 없는 상태입니다.");
    if (!["paid", "done", "noshow"].includes(b.status)) fail(409, "취소된 상담은 바꿀 수 없습니다.");
    db.prepare("UPDATE bookings SET status = ? WHERE id = ?").run(status, b.id);
    if (status === "done" && b.status !== "done") addMessage(b.id, "system", "상담이 종료됐습니다. 이야기해 주셔서 고맙습니다.");
    res.json({ booking: publicBooking({ ...b, status }) });
  });

  app.post("/api/admin/bookings/:id/refund", requireAdmin, ah(async (req, res) => {
    const b = adminBooking(req);
    if (!["paid", "done", "noshow"].includes(b.status)) fail(409, "환불할 수 없는 상태입니다.");
    const amount = req.body.amount ? Math.floor(Number(req.body.amount)) : b.amount;
    if (!(amount > 0 && amount <= b.amount)) fail(400, "환불 금액을 확인해 주세요.");
    await refund(b, String(req.body.reason || "상담사 환불").slice(0, 200), amount);
    res.json({ ok: true });
  }));

  // 상담 가능 시간표 (오늘부터 bookAheadDays일)
  app.get("/api/admin/slots", requireAdmin, (_req, res) => {
    expireHolds();
    const open = new Set(db.prepare("SELECT starts_at FROM slots WHERE starts_at >= ?").all(new Date(now() - DAY).toISOString()).map((r) => r.starts_at));
    const booked = new Map(db.prepare(`SELECT b.starts_at, b.status, u.nickname FROM bookings b JOIN users u ON u.id = b.user_id
      WHERE b.status IN ('pending','paid','done','noshow') AND b.starts_at >= ?`).all(new Date(now() - DAY).toISOString()).map((r) => [r.starts_at, r]));
    const days = [];
    for (let i = 0; i <= RULES.bookAheadDays; i++) {
      const date = kstDate(new Date(now() + i * DAY));
      days.push({
        date,
        hours: RULES.slotHours.map((h) => {
          const startsAt = kstIso(date, h);
          const bk = booked.get(startsAt);
          return {
            hour: h, startsAt,
            past: Date.parse(startsAt) < now(),
            open: open.has(startsAt),
            booked: bk ? { status: bk.status, nickname: bk.nickname } : null,
          };
        }),
      });
    }
    res.json({ days });
  });

  app.put("/api/admin/slots", requireAdmin, (req, res) => {
    const items = Array.isArray(req.body.items) ? req.body.items.slice(0, 500) : [];
    tx(db, () => {
      for (const { startsAt, open } of items) {
        const t = Date.parse(startsAt);
        if (!Number.isFinite(t) || new Date(t).toISOString() !== startsAt) continue;
        if (open) db.prepare("INSERT OR IGNORE INTO slots (starts_at) VALUES (?)").run(startsAt);
        else db.prepare("DELETE FROM slots WHERE starts_at = ?").run(startsAt);
      }
    });
    res.json({ ok: true });
  });

  // ═════════════ 화면 ═════════════
  const pub = join(HERE, "public");
  app.use(express.static(pub, { extensions: ["html"], index: "index.html" }));
  app.get(["/pay/success", "/pay/fail"], (_req, res) => res.sendFile(join(pub, "index.html")));
  app.use("/api", (_req, _res, next) => next(new HttpError(404, "없는 주소입니다.")));

  app.use((err, _req, res, _next) => {
    const status = err.status || (err.type === "entity.parse.failed" ? 400 : 500);
    if (status >= 500 && !(err instanceof HttpError)) console.error(err);
    res.status(status).json({ error: status >= 500 && !(err instanceof HttpError) ? "서버 오류가 났습니다. 잠시 뒤 다시 해 주세요." : err.message });
  });

  app.locals.db = db;
  return app;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const app = createApp();
  app.listen(C.PORT, () => {
    console.log(`상담 앱 실행 중: ${C.BASE_URL}  (관리자: ${C.BASE_URL}/admin, 결제: ${C.PAYMENT_MODE})`);
    if (!C.ADMIN_PASSWORD) console.warn("⚠️  ADMIN_PASSWORD가 비어 있어 관리자 로그인이 막혀 있습니다.");
  });
}
