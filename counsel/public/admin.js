import { h, api, fmtWhen, fmtWeekday, won, STATUS, toast, beep, chatRoom } from "./shared.js";

const view = document.getElementById("view");
const nav = document.getElementById("admin-nav");
let cleanup = null;
let openId = null; // 지금 보고 있는 상담
const unread = new Set(JSON.parse(localStorage.getItem("unread") || "[]"));
const saveUnread = () => { try { localStorage.setItem("unread", JSON.stringify([...unread])); } catch {} };

function render(...nodes) {
  cleanup?.(); cleanup = null;
  view.replaceChildren(...nodes);
  const r = location.hash.replace(/^#\/?/, "").split("/")[0];
  for (const a of nav.querySelectorAll("a")) a.classList.toggle("on", a.getAttribute("href") === "#/" + (r === "b" ? "" : r));
}
const page = (...kids) => h("main", {}, h("div", { class: "wrap wide stack-lg" }, ...kids));

async function boot() {
  const { admin } = await api("/api/admin/me");
  if (!admin) return loginView();
  nav.hidden = false;
  listen();
  addEventListener("hashchange", route);
  route();
}

function loginView() {
  const pw = h("input", { type: "password", autocomplete: "current-password", required: true });
  const err = h("p", { class: "error", role: "alert" });
  render(h("main", {}, h("div", { class: "wrap" }, h("form", { class: "card stack", onsubmit: async (e) => {
    e.preventDefault(); err.textContent = "";
    try { await api("/api/admin/login", { method: "POST", body: { password: pw.value } }); boot(); }
    catch (e2) { err.textContent = e2.message; }
  } }, h("h1", {}, "상담사 로그인"), h("label", { class: "field" }, h("span", {}, "관리자 비밀번호"), pw), err,
    h("button", { class: "btn block" }, "들어가기")))));
}

// 새 예약·새 메시지 알림
function listen() {
  const es = new EventSource("/api/admin/stream");
  es.addEventListener("booking", (e) => {
    const b = JSON.parse(e.data);
    if (b.nickname) alertMe(`새 예약: ${b.nickname} · ${fmtWhen(b.startsAt)}`, `#/b/${b.id}`);
    if (!openId) refreshList();
  });
  es.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.sender !== "user") return;
    if (m.bookingId === openId && !document.hidden) return;
    unread.add(m.bookingId); saveUnread();
    alertMe(`새 메시지: ${m.body.slice(0, 60)}`, `#/b/${m.bookingId}`);
    refreshList();
  });
}

function alertMe(text, href) {
  beep();
  toast(text);
  if ("Notification" in window && Notification.permission === "granted" && document.hidden) {
    const n = new Notification("상담 알림", { body: text, icon: "/icons/icon-192.png" });
    n.onclick = () => { focus(); location.hash = href; n.close(); };
  }
}

function notifyButton() {
  if (!("Notification" in window) || Notification.permission !== "default") return null;
  const b = h("button", { class: "btn sm quiet", onclick: async () => { await Notification.requestPermission(); b.remove(); } }, "🔔 알림 켜기");
  return b;
}

let refreshList = () => {};

function route() {
  const [name, arg] = location.hash.replace(/^#\/?/, "").split("/");
  openId = null;
  if (name === "slots") return slotsView();
  if (name === "past") return listView("past");
  if (name === "b") return listView("upcoming", arg);
  return listView("upcoming");
}

// ───────── 상담 목록 + 상세 ─────────
async function listView(scope, selectedId) {
  const listBox = h("div", { class: "list" });
  const detailBox = h("div");
  const narrow = matchMedia("(max-width: 899px)").matches;

  async function drawList() {
    const { bookings } = await api(`/api/admin/bookings?scope=${scope}`);
    const groups = new Map();
    for (const b of bookings) {
      const key = fmtWhen(b.startsAt).replace(/\s*(오전|오후).*/, "");
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(b);
    }
    listBox.replaceChildren(...(bookings.length ? [...groups].flatMap(([day, items]) => [
      h("h3", { class: "muted small" }, day),
      ...items.map((b) => {
        const [label, cls] = b.phase === "open" ? ["진행 중", "live"] : STATUS[b.status] || [b.status, "gray"];
        return h("button", { class: "card bk", "aria-current": String(b.id === selectedId), onclick: () => { location.hash = `#/b/${b.id}`; } },
          h("div", { class: "row spread" }, h("b", {}, fmtWhen(b.startsAt).replace(/^.*\)\s*/, "")), h("span", { class: `chip ${cls}` }, label)),
          h("div", { class: "row" }, unread.has(b.id) ? h("span", { class: "dot", title: "안 읽은 메시지" }) : null,
            h("span", {}, b.nickname), h("span", { class: "muted small" }, `${b.productName} · ${won(b.amount)}`)),
          h("div", { class: "muted small" }, b.intake.slice(0, 70) + (b.intake.length > 70 ? "…" : "")));
      })]) : [h("div", { class: "notice" }, scope === "past" ? "지난 상담이 없습니다." : "예정된 상담이 없습니다. '시간 열기'에서 상담 가능한 시간을 열어 주세요.")]));
  }
  refreshList = () => drawList().catch(() => {});

  const head = h("div", { class: "row spread" }, h("h1", {}, scope === "past" ? "지난 상담" : "예정된 상담"), notifyButton());
  if (selectedId && narrow) {
    render(page(h("a", { href: scope === "past" ? "#/past" : "#/" }, "← 목록"), detailBox));
  } else {
    render(page(head, h("div", { class: "admin-grid" }, listBox, detailBox)));
    await drawList();
  }
  if (selectedId) await detail(selectedId, detailBox, drawList);
  else detailBox.append(h("div", { class: "notice" }, "왼쪽에서 상담을 고르면 사연과 채팅이 여기 나옵니다."));
}

async function detail(id, box, redrawList) {
  openId = id;
  unread.delete(id); saveUnread();
  const data = await api(`/api/admin/bookings/${id}`);
  const b = data.booking;
  const actions = h("div", { class: "row" });
  const setStatus = async (status, msg) => {
    if (!confirm(msg)) return;
    try { const r = await api(`/api/admin/bookings/${id}/status`, { method: "POST", body: { status } }); chat.update(r.booking); drawActions(); redrawList().catch(() => {}); }
    catch (e) { toast(e.message); }
  };
  function drawActions() {
    actions.replaceChildren();
    if (b.status === "paid") {
      actions.append(
        h("button", { class: "btn sm quiet", onclick: () => setStatus("done", "상담 완료로 처리할까요? 고객 채팅 입력이 닫힙니다.") }, "완료 처리"),
        h("button", { class: "btn sm ghost", onclick: () => setStatus("noshow", "불참으로 처리할까요?") }, "불참"));
    }
    if (["done", "noshow"].includes(b.status)) actions.append(h("button", { class: "btn sm ghost", onclick: () => setStatus("paid", "다시 진행 중으로 돌릴까요?") }, "다시 열기"));
    if (["paid", "done", "noshow"].includes(b.status)) actions.append(h("button", { class: "btn sm danger", onclick: async () => {
      const amt = prompt(`환불 금액 (최대 ${b.amount}원)`, String(b.amount));
      if (!amt) return;
      const reason = prompt("환불 사유 (고객에게 보이지 않습니다)", "상담사 환불") || "상담사 환불";
      try { await api(`/api/admin/bookings/${id}/refund`, { method: "POST", body: { amount: Number(amt.replace(/\D/g, "")), reason } }); toast("환불했습니다."); route(); }
      catch (e) { toast(e.message); }
    } }, "환불"));
  }
  drawActions();

  const info = h("div", { class: "card stack" },
    h("div", { class: "row spread" }, h("h2", {}, b.nickname), h("span", { class: `chip ${STATUS[b.status]?.[1] || "gray"}` }, STATUS[b.status]?.[0] || b.status)),
    h("div", { class: "muted small" }, `${fmtWhen(b.startsAt)} · ${b.productName} · ${won(b.amount)} · ${b.email}`),
    b.history.length ? h("div", { class: "small" }, `이전 상담 ${b.history.length}회 — `, b.history.map((x, i) => [i ? ", " : "", h("a", { href: `#/b/${x.id}` }, fmtWhen(x.startsAt))])) : h("div", { class: "small muted" }, "첫 상담"),
    h("div", {}, h("h3", {}, "사전 사연"), h("div", { class: "intake" }, b.intake)),
    b.status === "canceled" ? h("div", { class: "notice" }, `취소됨 · ${b.cancelReason} · ${won(b.refundedAmount)} 환불`) : null,
    actions);

  const chat = chatRoom({
    who: "admin", booking: b, messages: data.messages, serverNow: data.serverNow,
    streamUrl: `/api/admin/bookings/${id}/stream`, sendUrl: `/api/admin/bookings/${id}/messages`,
    head: h("div", { class: "title" }, `${b.nickname} 님과의 채팅`),
  });
  box.replaceChildren(h("div", { class: "stack" }, info, chat));
  cleanup = chat.destroy;
}

// ───────── 상담 가능 시간 ─────────
async function slotsView() {
  const grid = h("div");
  const days = { 0: "일", 1: "월", 2: "화", 3: "수", 4: "목", 5: "금", 6: "토" };
  let data;

  async function load() { data = await api("/api/admin/slots"); draw(); }
  async function save(items) {
    try { await api("/api/admin/slots", { method: "PUT", body: { items } }); await load(); }
    catch (e) { toast(e.message); }
  }
  function draw() {
    grid.replaceChildren(...data.days.map((d) => {
      const editable = d.hours.filter((x) => !x.past && !x.booked);
      return h("div", { class: "slot-day" },
        h("div", { class: "d" }, `${+d.date.slice(5, 7)}/${+d.date.slice(8)} (${fmtWeekday(d.hours[0].startsAt)})`,
          editable.length ? h("small", {}, h("a", { href: "#", onclick: (e) => { e.preventDefault(); save(editable.map((x) => ({ startsAt: x.startsAt, open: !editable.every((y) => y.open) }))); } },
            editable.every((y) => y.open) ? "모두 닫기" : "모두 열기")) : null),
        h("div", { class: "slot-hours" }, d.hours.map((x) => h("button", {
          type: "button",
          class: "slot" + (x.booked ? " booked" : x.open ? " open" : ""),
          disabled: x.past || !!x.booked,
          title: x.booked ? `${x.booked.nickname} (${x.booked.status === "pending" ? "결제 중" : "예약"})` : x.open ? "열림 — 누르면 닫힘" : "닫힘 — 누르면 열림",
          onclick: () => save([{ startsAt: x.startsAt, open: !x.open }]),
        }, x.booked ? x.booked.nickname.slice(0, 4) : `${x.hour}시`))));
    }));
  }

  // 요일·시간대로 한꺼번에
  const picks = h("div", { class: "weekday-picks" }, [1, 2, 3, 4, 5, 6, 0].map((n) => h("label", {}, h("input", { type: "checkbox", value: n, checked: n >= 1 && n <= 5 }), days[n])));
  const hourOpts = (sel) => Array.from({ length: 14 }, (_, i) => i + 10).map((hh) => h("option", { value: hh, selected: hh === sel }, `${hh}시`));
  const from = h("select", { "aria-label": "시작 시각" }, hourOpts(20));
  const to = h("select", { "aria-label": "마지막 시각" }, hourOpts(22));
  const bulk = (open) => {
    const wds = new Set([...picks.querySelectorAll("input:checked")].map((i) => days[i.value]));
    const lo = Number(from.value), hi = Number(to.value);
    const items = data.days.flatMap((d) => d.hours.filter((x) => !x.past && !x.booked && x.hour >= lo && x.hour <= hi && wds.has(fmtWeekday(x.startsAt))))
      .map((x) => ({ startsAt: x.startsAt, open }));
    if (!items.length) return toast("해당하는 시간이 없습니다.");
    save(items).then(() => toast(`${items.length}개 시간을 ${open ? "열었" : "닫았"}습니다.`));
  };

  render(page(
    h("h1", {}, "상담 가능 시간"),
    h("div", { class: "card stack" },
      h("h3", {}, "한꺼번에 열기"),
      picks,
      h("div", { class: "row" }, from, "부터", to, "까지 (시작 시각 기준)"),
      h("div", { class: "row" }, h("button", { class: "btn sm", onclick: () => bulk(true) }, "2주 동안 열기"), h("button", { class: "btn sm ghost", onclick: () => bulk(false) }, "닫기"))),
    h("div", { class: "stack" },
      h("div", { class: "legend" }, h("span", {}, h("i", { style: "background:var(--ok-bg);border-color:var(--ok)" }), "열림 (예약 가능)"),
        h("span", {}, h("i", {}), "닫힘"), h("span", {}, h("i", { style: "background:var(--plum);border-color:var(--plum)" }), "예약됨")),
      h("p", { class: "muted small" }, "칸을 누르면 열고 닫힙니다. 고객은 지금부터 3시간 뒤 ~ 14일 안의 열린 시간만 볼 수 있어요. 한 칸 = 1시간."),
      grid),
  ));
  await load();
}

boot().catch((e) => render(page(h("div", { class: "notice err" }, e.message))));
