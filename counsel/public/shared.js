// 고객 화면과 관리자 화면이 같이 쓰는 도구들

export const TZ = "Asia/Seoul";

// 요소 만들기. 글자는 항상 textContent로 들어가므로 사용자가 쓴 내용이 HTML로 해석되지 않습니다.
export function h(tag, props = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (v == null || v === false) continue;
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "dataset") Object.assign(el.dataset, v);
    else if (k in el && typeof v !== "string") el[k] = v;
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat(Infinity)) {
    if (kid == null || kid === false) continue;
    el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return el;
}

export async function api(path, { method = "GET", body } = {}) {
  const res = await fetch(path, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
    credentials: "same-origin",
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.error || "연결이 잠시 불안정합니다. 다시 시도해 주세요.");
    err.status = res.status;
    throw err;
  }
  return data;
}

const fmt = (opts) => new Intl.DateTimeFormat("ko-KR", { timeZone: TZ, ...opts });
export const fmtWhen = (iso) => fmt({ month: "long", day: "numeric", weekday: "short", hour: "numeric", minute: "2-digit" }).format(new Date(iso));
export const fmtTime = (iso) => fmt({ hour: "numeric", minute: "2-digit" }).format(new Date(iso));
export const fmtWeekday = (iso) => fmt({ weekday: "short" }).format(new Date(iso));
export const kstDate = (iso) => new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(iso));
export const won = (n) => n.toLocaleString("ko-KR") + "원";

export function fmtLeft(ms) {
  if (ms < 0) ms = 0;
  const s = Math.floor(ms / 1000);
  const d = Math.floor(s / 86400), hh = Math.floor((s % 86400) / 3600), mm = Math.floor((s % 3600) / 60), ss = s % 60;
  if (d > 0) return `${d}일 ${hh}시간`;
  if (hh > 0) return `${hh}시간 ${mm}분`;
  return `${mm}:${String(ss).padStart(2, "0")}`;
}

export const STATUS = {
  paid: ["예약 확정", "ok"],
  done: ["상담 완료", "gray"],
  noshow: ["불참", "warn"],
  canceled: ["취소·환불", "gray"],
};

export function toast(text, ms = 3200) {
  const el = h("div", { class: "toast", role: "status" }, text);
  document.body.append(el);
  setTimeout(() => el.remove(), ms);
}

export function beep() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.value = 880; g.gain.value = 0.08;
    o.connect(g).connect(ctx.destination);
    o.start(); o.stop(ctx.currentTime + 0.18);
  } catch {}
}

// 채팅방. who = "user" | "admin" (내 쪽)
export function chatRoom({ who, booking, messages, serverNow, streamUrl, sendUrl, enterBeforeMin = 10, head, onChange }) {
  const skew = Date.parse(serverNow) - Date.now(); // 휴대폰 시계가 틀려도 서버 시간 기준으로
  const now = () => Date.now() + skew;
  const seen = new Set();
  const list = h("div", { class: "msgs", "aria-live": "polite" });
  const timer = h("span", { class: "timer" });
  const bottom = h("div");

  function phase() {
    if (booking.status !== "paid") return "closed";
    const t = now(), s = Date.parse(booking.startsAt), e = Date.parse(booking.endsAt);
    if (t < s - enterBeforeMin * 60000) return "waiting";
    if (t <= e) return "open";
    return "ended";
  }

  function bubble(m) {
    if (seen.has(m.id)) return;
    seen.add(m.id);
    const mine = m.sender === who;
    const cls = m.sender === "system" ? "system" : mine ? "me" : "them";
    const label = !mine && m.sender === "admin" ? "상담사" : !mine && m.sender === "user" ? booking.nickname || "고객" : null;
    const stick = list.scrollHeight - list.scrollTop - list.clientHeight < 80;
    list.append(h("div", { class: `msg ${cls}` }, label && cls === "them" ? h("span", { class: "who" }, label) : null, m.body,
      cls !== "system" ? h("time", {}, fmtTime(m.createdAt)) : null));
    if (stick || mine) list.scrollTop = list.scrollHeight;
  }
  messages.forEach(bubble);

  const input = h("textarea", { rows: 1, placeholder: "메시지를 입력하세요", "aria-label": "메시지", maxlength: who === "admin" ? 4000 : 2000 });
  const send = h("button", { class: "btn", type: "submit" }, "보내기");
  const form = h("form", { class: "composer", onsubmit: async (e) => {
    e.preventDefault();
    const body = input.value.trim();
    if (!body) return;
    send.disabled = true;
    try {
      const { message } = await api(sendUrl, { method: "POST", body: { body } });
      input.value = ""; input.style.height = "";
      bubble(message);
    } catch (err) { toast(err.message); }
    finally { send.disabled = false; input.focus(); }
  } }, input, send);
  input.addEventListener("input", () => { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 160) + "px"; });
  input.addEventListener("keydown", (e) => {
    // 컴퓨터에서는 Enter로 보내기, Shift+Enter 줄바꿈 (휴대폰은 보내기 버튼)
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing && matchMedia("(pointer: fine)").matches) { e.preventDefault(); form.requestSubmit(); }
  });

  let lastPhase = null;
  function tick() {
    const p = phase();
    const s = Date.parse(booking.startsAt), e = Date.parse(booking.endsAt);
    if (p === "waiting") timer.textContent = `시작까지 ${fmtLeft(s - now())}`;
    else if (p === "open") timer.textContent = now() < s ? `곧 시작 · ${fmtLeft(s - now())}` : `남은 시간 ${fmtLeft(e - now())}`;
    else if (p === "ended") timer.textContent = "상담 시간 종료";
    else timer.textContent = STATUS[booking.status]?.[0] || "";
    if (p !== lastPhase) {
      lastPhase = p;
      const canSend = who === "admin" ? booking.status === "paid" : p === "open";
      bottom.replaceChildren(canSend ? form : h("div", { class: "composer-note" },
        p === "waiting" ? `상담 시작 ${enterBeforeMin}분 전부터 메시지를 보낼 수 있습니다.`
        : p === "ended" ? "상담 시간이 끝났습니다. 대화 내용은 계속 볼 수 있어요."
        : booking.status === "canceled" ? "취소된 상담입니다." : "종료된 상담입니다."));
      onChange?.(p);
    }
  }
  tick();
  const iv = setInterval(tick, 1000);

  // 실시간 수신 + 끊겼다 다시 붙으면 놓친 메시지 채우기
  const es = new EventSource(streamUrl);
  es.addEventListener("message", (e) => bubble(JSON.parse(e.data)));
  es.addEventListener("open", async () => {
    try {
      const data = await api(sendUrl.replace(/\/messages$/, ""));
      data.messages.forEach(bubble);
      if (data.booking.status !== booking.status) { Object.assign(booking, data.booking); lastPhase = null; tick(); }
    } catch {}
  });

  const root = h("section", { class: "room" }, h("div", { class: "room-head" }, head, h("div", {}, timer)), list, bottom);
  requestAnimationFrame(() => { list.scrollTop = list.scrollHeight; });
  root.destroy = () => { clearInterval(iv); es.close(); };
  root.update = (b) => { Object.assign(booking, b); lastPhase = null; tick(); };
  return root;
}

export function icsFor(booking, title) {
  const z = (iso) => iso.replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const ics = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//counsel//KO", "BEGIN:VEVENT",
    `UID:${booking.id}@counsel`, `DTSTAMP:${z(new Date().toISOString())}`,
    `DTSTART:${z(booking.startsAt)}`, `DTEND:${z(booking.endsAt)}`,
    `SUMMARY:${title}`, `DESCRIPTION:${location.origin}/#/room/${booking.id}`,
    "BEGIN:VALARM", "TRIGGER:-PT15M", "ACTION:DISPLAY", `DESCRIPTION:${title}`, "END:VALARM",
    "END:VEVENT", "END:VCALENDAR",
  ].join("\r\n");
  return URL.createObjectURL(new Blob([ics], { type: "text/calendar" }));
}
