import { h, api, fmtWhen, fmtWeekday, fmtTime, kstDate, won, STATUS, toast, chatRoom, icsFor } from "./shared.js";

const view = document.getElementById("view");
const state = { config: null, user: null, draft: { product: null, startsAt: null, intake: "", agree: {} } };
let cleanup = null;

async function boot() {
  [state.config, { user: state.user }] = await Promise.all([api("/api/config"), api("/api/me")]);
  if (state.config.products.length && !state.draft.product) state.draft.product = state.config.products[0].id;
  addEventListener("hashchange", route);
  route();
}

function setNav() {
  document.getElementById("nav-login").hidden = !!state.user;
  const r = location.hash.slice(2).split("/")[0];
  document.getElementById("nav-me").classList.toggle("on", r === "me" || r === "room");
}

function render(...nodes) {
  cleanup?.(); cleanup = null;
  view.replaceChildren(...nodes);
  scrollTo(0, 0);
  setNav();
}

const page = (...kids) => h("main", {}, h("div", { class: "wrap stack-lg" }, ...kids));
const foot = () => h("footer", { class: "foot" },
  h("a", { href: "#/terms" }, "이용약관"), " · ", h("a", { href: "#/privacy" }, "개인정보 처리방침"), " · ",
  h("a", { href: "https://www.instagram.com/mszexc/", target: "_blank", rel: "noopener" }, "@mszexc"));

function route() {
  const path = location.pathname;
  if (path === "/pay/success") return paySuccess();
  if (path === "/pay/fail") return payFail();
  const [name, arg] = location.hash.replace(/^#\/?/, "").split("/");
  ({ "": home, book, login: () => login(), me, room: () => room(arg), pay, terms, privacy }[name] || home)();
}

// ───────── 첫 화면 ─────────
function home() {
  const products = state.config.products;
  render(page(
    h("section", { class: "hero" },
      h("p", { class: "eyebrow" }, "「남자들끼리 하는 말」 박지훈 · 1:1 채팅 상담"),
      h("h1", {}, "DM 대신,", h("br"), "정해진 시간에 1:1로."),
      h("p", { class: "lead" }, "DM으로는 답이 늦거나 묻히기 쉽습니다. 시간을 예약하면 그 시간 동안은 당신 이야기만 봅니다."),
      h("a", { class: "btn block", href: "#/book" }, "상담 시간 예약하기"),
    ),
    h("section", { class: "card stack" },
      h("h2", {}, "이렇게 진행돼요"),
      h("ol", { class: "steps" },
        h("li", {}, h("div", {}, h("b", {}, "시간 고르기"), h("br"), h("span", { class: "muted small" }, "열려 있는 시간 중 편한 때를 고릅니다."))),
        h("li", {}, h("div", {}, h("b", {}, "상황 적고 결제"), h("br"), h("span", { class: "muted small" }, "미리 읽고 들어가니 첫 10분을 아낄 수 있어요."))),
        h("li", {}, h("div", {}, h("b", {}, "예약한 시간에 채팅"), h("br"), h("span", { class: "muted small" }, `시작 ${state.config.rules.enterBeforeMin}분 전부터 채팅방이 열립니다. 대화 내용은 끝난 뒤에도 다시 볼 수 있어요.`))),
      ),
    ),
    h("section", { class: "stack" },
      h("h2", {}, "상담 종류"),
      h("div", { class: "choices" }, products.map((p) => h("div", { class: "choice" },
        h("div", { class: "row spread" }, h("span", { class: "name" }, p.name), h("span", { class: "price" }, won(p.price))),
        h("div", { class: "desc" }, p.desc)))),
      h("p", { class: "muted small" }, `시작 ${state.config.rules.freeCancelHours}시간 전까지는 직접 취소하면 전액 환불됩니다.`),
    ),
    crisisNotice(),
    h("a", { class: "btn block", href: "#/book" }, "상담 시간 예약하기"),
  ), foot());
}

function crisisNotice() {
  return h("div", { class: "notice warn" },
    h("strong", {}, "이 상담은 의료·심리치료가 아닙니다"),
    "연애와 관계에 대한 대화입니다. 스스로를 해치고 싶은 마음이 들거나 위급하다면 지금 바로 ",
    h("a", { href: "tel:109" }, "자살예방상담전화 109"), " 또는 ", h("a", { href: "tel:119" }, "119"), "에 연락해 주세요. 24시간 받습니다.");
}

// ───────── 예약 ─────────
async function book() {
  const d = state.draft;
  render(page(h("p", { class: "muted" }, "열린 시간을 불러오는 중…")));
  let slots;
  try { ({ slots } = await api("/api/slots")); }
  catch (e) { return render(page(h("div", { class: "notice err" }, e.message))); }
  if (d.startsAt && !slots.includes(d.startsAt)) d.startsAt = null;

  const days = [...new Set(slots.map(kstDate))];
  let day = d.startsAt ? kstDate(d.startsAt) : days[0];
  const err = h("p", { class: "error", role: "alert" });

  // 1. 상품
  const productBox = h("div", { class: "choices", role: "radiogroup" }, state.config.products.map((p) =>
    h("label", { class: "choice" },
      h("input", { type: "radio", name: "product", value: p.id, checked: d.product === p.id, onchange: () => { d.product = p.id; } }),
      h("div", { class: "row spread" }, h("span", { class: "name" }, p.name), h("span", { class: "price" }, won(p.price))),
      h("div", { class: "desc" }, p.desc))));

  // 2. 날짜·시간
  const dayRow = h("div", { class: "days" });
  const timeGrid = h("div", { class: "times" });
  function drawTimes() {
    dayRow.replaceChildren(...days.map((dd) => {
      const first = slots.find((s) => kstDate(s) === dd);
      return h("button", { type: "button", class: "day", "aria-pressed": String(dd === day), onclick: () => { day = dd; drawTimes(); } },
        h("b", {}, `${+dd.slice(5, 7)}/${+dd.slice(8)}`), h("small", {}, fmtWeekday(first)));
    }));
    timeGrid.replaceChildren(...slots.filter((s) => kstDate(s) === day).map((s) =>
      h("button", { type: "button", class: "time", "aria-pressed": String(s === d.startsAt), onclick: () => { d.startsAt = s; drawTimes(); } }, fmtTime(s))));
  }
  drawTimes();

  // 3. 사연
  const intake = h("textarea", { id: "intake", placeholder: "예) 3년 만난 여자친구와 2주 전 헤어졌어요. 이별 통보는 카톡으로 받았고, 그 뒤로 연락은 안 했습니다. 다시 연락해도 될지, 한다면 언제 뭐라고 해야 할지 알고 싶어요.", maxlength: 3000 });
  intake.value = d.intake;
  intake.addEventListener("input", () => { d.intake = intake.value; });

  // 4. 동의
  const agree = (key, ...label) => h("label", { class: "check" },
    h("input", { type: "checkbox", checked: !!d.agree[key], onchange: (e) => { d.agree[key] = e.target.checked; } }), h("span", {}, ...label));

  // 5. 로그인 + 결제
  const authBox = h("div");
  function drawAuth() {
    authBox.replaceChildren(state.user
      ? h("p", { class: "muted small" }, `${state.user.nickname}(${state.user.email})으로 예약합니다.`)
      : h("div", { class: "card stack" }, h("h3", {}, "예약 내역을 다시 보려면 계정이 필요해요"), authForm(() => drawAuth())));
  }
  drawAuth();

  const submit = h("button", { class: "btn block", type: "button", onclick: async () => {
    err.textContent = "";
    if (!d.startsAt) return (err.textContent = "시간을 골라 주세요.");
    if (d.intake.trim().length < 10) { intake.focus(); return (err.textContent = "상황을 10자 이상 적어 주세요."); }
    if (!d.agree.terms || !d.agree.sensitive || !d.agree.crisis) return (err.textContent = "필수 동의 항목을 확인해 주세요.");
    if (!state.user) return (err.textContent = "위에서 가입하거나 로그인해 주세요.");
    submit.disabled = true;
    try {
      const order = await api("/api/bookings", { method: "POST", body: {
        product: d.product, startsAt: d.startsAt, intake: d.intake,
        agreeTerms: true, agreeSensitive: true, agreeCrisis: true,
      } });
      sessionStorage.setItem("order", JSON.stringify({ ...order, startsAt: d.startsAt, at: Date.now() }));
      location.hash = "#/pay";
    } catch (e) {
      err.textContent = e.message;
      if (e.status === 409) book();
    } finally { submit.disabled = false; }
  } }, "결제하기");

  render(page(
    h("h1", {}, "상담 예약"),
    h("section", { class: "stack" }, h("h2", {}, "1. 상담 종류"), productBox),
    h("section", { class: "stack" }, h("h2", {}, "2. 시간"),
      slots.length ? [dayRow, timeGrid, h("p", { class: "muted small" }, "모든 시간은 한국 시간입니다.")]
        : h("div", { class: "notice" }, h("strong", {}, "지금은 열린 시간이 없어요"), "새 시간은 인스타그램 스토리로 먼저 알려드립니다.")),
    h("section", { class: "stack" }, h("h2", {}, "3. 지금 상황"),
      h("p", { class: "muted small" }, "어떤 관계였는지, 지금 어떤 상황인지, 마지막 연락은 언제였는지, 상담에서 무엇을 얻고 싶은지 적어 주세요. 상담사만 읽습니다."),
      intake),
    h("section", { class: "stack" }, h("h2", {}, "4. 확인해 주세요"),
      crisisNotice(),
      agree("crisis", "(필수) 위 내용을 읽었고, 이 상담이 의료·심리치료가 아님을 이해했습니다."),
      agree("sensitive", "(필수) 상담을 위해 제가 적은 연애·심리 관련 내용(민감정보)을 수집·이용하는 데 동의합니다. ", h("a", { href: "#/privacy", target: "_blank" }, "자세히")),
      agree("terms", "(필수) ", h("a", { href: "#/terms", target: "_blank" }, "이용약관과 환불 규정"), `에 동의합니다. 시작 ${state.config.rules.freeCancelHours}시간 전까지 취소하면 전액 환불됩니다.`)),
    authBox,
    h("div", { class: "stack" }, err, submit),
  ));
}

function authForm(done) {
  let mode = "signup";
  const tabs = h("div", { class: "tabs", role: "tablist" });
  const email = h("input", { type: "email", autocomplete: "email", required: true });
  const pw = h("input", { type: "password", autocomplete: "new-password", minlength: 8, required: true });
  const nick = h("input", { type: "text", maxlength: 20, autocomplete: "nickname", placeholder: "실명이 아니어도 됩니다" });
  const nickField = h("label", { class: "field" }, h("span", {}, "닉네임"), nick);
  const err = h("p", { class: "error", role: "alert" });
  const btn = h("button", { class: "btn block", type: "submit" });
  function draw() {
    tabs.replaceChildren(
      h("button", { type: "button", role: "tab", "aria-selected": String(mode === "signup"), onclick: () => { mode = "signup"; draw(); } }, "처음이에요"),
      h("button", { type: "button", role: "tab", "aria-selected": String(mode === "login"), onclick: () => { mode = "login"; draw(); } }, "로그인"));
    nickField.hidden = mode !== "signup";
    pw.autocomplete = mode === "signup" ? "new-password" : "current-password";
    btn.textContent = mode === "signup" ? "가입하기" : "로그인";
    err.textContent = "";
  }
  draw();
  return h("form", { class: "stack", onsubmit: async (e) => {
    e.preventDefault();
    btn.disabled = true; err.textContent = "";
    try {
      const { user } = await api(mode === "signup" ? "/api/signup" : "/api/login", { method: "POST",
        body: { email: email.value, password: pw.value, nickname: nick.value } });
      state.user = user;
      setNav();
      done();
    } catch (e2) { err.textContent = e2.message; }
    finally { btn.disabled = false; }
  } }, tabs,
    h("label", { class: "field" }, h("span", {}, "이메일"), email),
    h("label", { class: "field" }, h("span", {}, "비밀번호 (8자 이상)"), pw),
    nickField, err, btn);
}

function login() {
  if (state.user) return (location.hash = "#/me");
  render(page(h("h1", {}, "로그인"), h("div", { class: "card" }, authForm(() => { location.hash = "#/me"; }))), foot());
}

// ───────── 결제 ─────────
async function pay() {
  const order = JSON.parse(sessionStorage.getItem("order") || "null");
  if (!order) return (location.hash = "#/book");
  const err = h("p", { class: "error", role: "alert" });
  const summary = h("div", { class: "card stack" },
    h("div", { class: "row spread" }, h("b", {}, order.orderName.split(" · ")[0]), h("b", {}, won(order.amount))),
    h("div", { class: "muted" }, fmtWhen(order.startsAt)),
    h("p", { class: "muted small" }, "이 시간은 15분 동안 다른 분이 예약하지 못하게 잡아 두었습니다."));

  if (state.config.paymentMode === "mock") {
    render(page(h("h1", {}, "결제"), summary,
      h("div", { class: "notice warn" }, h("strong", {}, "테스트 모드"), "실제 결제가 일어나지 않습니다. 서버 설정에서 PAYMENT_MODE=toss로 바꾸면 토스페이먼츠 결제창이 나옵니다."),
      h("button", { class: "btn block", onclick: () => {
        const q = new URLSearchParams({ paymentKey: "mock_" + crypto.randomUUID().replace(/-/g, ""), orderId: order.orderId, amount: order.amount });
        location.href = "/pay/success?" + q;
      } }, `테스트 결제하기 · ${won(order.amount)}`), err));
    return;
  }

  const methods = h("div", { id: "payment-method" });
  const agreement = h("div", { id: "agreement" });
  const btn = h("button", { class: "btn block", disabled: true }, `${won(order.amount)} 결제하기`);
  render(page(h("h1", {}, "결제"), summary, h("div", {}, methods, agreement), err, btn));
  try {
    await loadScript("https://js.tosspayments.com/v2/standard");
    const widgets = window.TossPayments(state.config.tossClientKey).widgets({ customerKey: order.customerKey });
    await widgets.setAmount({ currency: "KRW", value: order.amount });
    await Promise.all([
      widgets.renderPaymentMethods({ selector: "#payment-method", variantKey: "DEFAULT" }),
      widgets.renderAgreement({ selector: "#agreement", variantKey: "AGREEMENT" }),
    ]);
    btn.disabled = false;
    btn.onclick = async () => {
      err.textContent = "";
      try {
        await widgets.requestPayment({
          orderId: order.orderId, orderName: order.orderName,
          customerName: order.customerName, customerEmail: order.customerEmail,
          successUrl: location.origin + "/pay/success", failUrl: location.origin + "/pay/fail",
        });
      } catch (e) { if (e.code !== "USER_CANCEL") err.textContent = e.message; }
    };
  } catch (e) {
    err.textContent = "결제창을 불러오지 못했습니다. 새로고침해 주세요. (" + e.message + ")";
  }
}

function loadScript(src) {
  return new Promise((ok, no) => {
    if (document.querySelector(`script[src="${src}"]`)) return ok();
    document.head.append(h("script", { src, onload: ok, onerror: () => no(new Error("스크립트 로드 실패")) }));
  });
}

async function paySuccess() {
  render(page(h("p", { class: "muted" }, "결제를 확인하는 중입니다. 창을 닫지 마세요…")));
  const q = new URLSearchParams(location.search);
  try {
    const { booking } = await api("/api/payments/confirm", { method: "POST",
      body: { paymentKey: q.get("paymentKey"), orderId: q.get("orderId"), amount: Number(q.get("amount")) } });
    sessionStorage.removeItem("order");
    state.draft = { product: state.draft.product, startsAt: null, intake: "", agree: {} };
    history.replaceState(null, "", "/#/room/" + booking.id);
    toast("예약이 확정됐습니다.");
    route();
  } catch (e) {
    render(page(h("h1", {}, "결제를 마치지 못했어요"), h("div", { class: "notice err" }, e.message),
      h("a", { class: "btn block", href: "/#/book" }, "다시 예약하기")));
  }
}

function payFail() {
  const q = new URLSearchParams(location.search);
  const msg = q.get("code") === "PAY_PROCESS_CANCELED" ? "결제를 취소하셨습니다." : q.get("message") || "결제가 완료되지 않았습니다.";
  render(page(h("h1", {}, "결제가 되지 않았어요"), h("div", { class: "notice" }, msg),
    h("a", { class: "btn block", href: "/#/pay" }, "다시 결제하기"), h("a", { class: "btn ghost block", href: "/#/book" }, "시간 다시 고르기")));
}

// ───────── 내 상담 ─────────
async function me() {
  if (!state.user) return (location.hash = "#/login");
  render(page(h("p", { class: "muted" }, "불러오는 중…")));
  const { bookings } = await api("/api/bookings");
  const upcoming = bookings.filter((b) => b.status === "paid" && b.phase !== "ended").reverse();
  const past = bookings.filter((b) => !upcoming.includes(b));
  const card = (b) => {
    const [label, cls] = b.phase === "open" ? ["지금 입장 가능", "live"] : STATUS[b.status] || [b.status, "gray"];
    return h("a", { class: "card item", href: `#/room/${b.id}` },
      h("div", { class: "row spread" }, h("span", { class: "when" }, fmtWhen(b.startsAt)), h("span", { class: `chip ${cls}` }, label)),
      h("div", { class: "muted small" }, `${b.productName} · ${won(b.amount)}`));
  };
  render(page(
    h("div", { class: "row spread" }, h("h1", {}, "내 상담"),
      h("button", { class: "btn sm ghost", onclick: async () => { await api("/api/logout", { method: "POST" }); state.user = null; location.hash = "#/"; } }, "로그아웃")),
    upcoming.length ? h("div", { class: "list" }, upcoming.map(card))
      : h("div", { class: "notice" }, h("strong", {}, "예정된 상담이 없어요"), h("a", { href: "#/book" }, "상담 시간 예약하기")),
    past.length ? h("section", { class: "stack" }, h("h2", {}, "지난 상담"), h("div", { class: "list" }, past.map(card))) : null,
    h("a", { class: "btn block", href: "#/book" }, "새 상담 예약하기"),
  ), foot());
}

async function room(id) {
  if (!state.user) return (location.hash = "#/login");
  let data;
  try { data = await api(`/api/bookings/${id}`); }
  catch (e) { return render(page(h("div", { class: "notice err" }, e.message), h("a", { class: "btn block", href: "#/me" }, "내 상담으로"))); }
  const b = data.booking;
  const extra = h("div", { class: "row small" });
  const title = `${b.productName} · ${fmtWhen(b.startsAt)}`;
  if (b.status === "paid" && b.phase !== "ended") extra.append(h("a", { href: icsFor(b, "1:1 채팅 상담"), download: "상담.ics" }, "캘린더에 추가"));
  if (b.canCancel) extra.append(h("button", { class: "btn sm danger", onclick: async () => {
    if (!confirm(`예약을 취소하고 ${won(b.amount)}을 환불받을까요?`)) return;
    try { const r = await api(`/api/bookings/${id}/cancel`, { method: "POST" }); chat.update(r.booking); toast("취소됐습니다. 환불은 카드사에 따라 3~7일 걸릴 수 있어요."); extra.replaceChildren(); }
    catch (e) { toast(e.message); }
  } }, "예약 취소"));
  const chat = chatRoom({
    who: "user", booking: b, messages: data.messages, serverNow: data.serverNow,
    streamUrl: `/api/bookings/${id}/stream`, sendUrl: `/api/bookings/${id}/messages`,
    enterBeforeMin: state.config.rules.enterBeforeMin,
    head: [h("div", { class: "row spread" }, h("a", { href: "#/me", "aria-label": "내 상담으로" }, "←"), h("span", { class: "title" }, title)), extra],
  });
  render(chat);
  cleanup = chat.destroy;
}

// ───────── 약관 ─────────
const F = (t) => h("span", { class: "fill" }, t); // 운영자가 채워야 하는 칸

function terms() {
  const r = state.config.rules;
  render(page(h("article", { class: "doc" },
    h("h1", {}, "이용약관"),
    h("p", { class: "muted small" }, "운영자: ", F("[상호]"), " · 대표 ", F("[이름]"), " · 사업자등록번호 ", F("[000-00-00000]"), " · 통신판매업 ", F("[제0000-지역-0000호]"), " · 문의 ", F("[이메일]")),
    h("h2", {}, "1. 서비스"),
    h("p", {}, "예약한 시간 동안 상담사와 1:1 채팅으로 연애·관계 고민을 이야기하는 서비스입니다. 의료행위나 심리치료가 아니며, 결과(재회 등)를 약속하지 않습니다."),
    h("h2", {}, "2. 예약과 결제"),
    h("p", {}, "상품을 고르고 결제가 승인되면 예약이 확정됩니다. 결제는 토스페이먼츠를 통해 처리됩니다."),
    h("h2", {}, "3. 취소·환불"),
    h("ul", {},
      h("li", {}, `상담 시작 ${r.freeCancelHours}시간 전까지: '내 상담'에서 직접 취소하면 전액 환불됩니다.`),
      h("li", {}, `그 이후: 원칙적으로 환불되지 않습니다. 부득이한 사정은 채팅방에 남겨 주시면 상담사가 판단합니다.`),
      h("li", {}, "상담사 사정으로 진행하지 못하면 전액 환불합니다."),
      h("li", {}, "시작 후 10분 동안 아무 응답이 없으면 불참으로 처리될 수 있습니다.")),
    h("h2", {}, "4. 이용 제한"),
    h("p", {}, "욕설·협박, 상대방을 해치려는 목적의 상담, 상담 내용의 무단 공개는 상담 중단 사유가 될 수 있습니다."),
    h("h2", {}, "5. 위급한 상황"),
    h("p", {}, "자신이나 다른 사람을 해칠 위험이 있다고 판단되면 상담을 멈추고 109·119 등 전문 기관 연락을 안내합니다."),
  )), foot());
}

function privacy() {
  render(page(h("article", { class: "doc" },
    h("h1", {}, "개인정보 처리방침"),
    h("h2", {}, "수집하는 정보"),
    h("ul", {},
      h("li", {}, "가입: 이메일, 닉네임, 비밀번호(암호화 저장)"),
      h("li", {}, "상담: 사전에 적은 사연과 채팅 내용 — 연애·심리 상태 등 민감정보가 포함될 수 있어 별도 동의를 받습니다."),
      h("li", {}, "결제: 주문번호, 금액, 결제 키 (카드번호는 토스페이먼츠가 처리하며 저희는 받지 않습니다)")),
    h("h2", {}, "이용 목적"),
    h("p", {}, "상담 진행, 예약 확인, 결제·환불 처리, 분쟁 대응에만 씁니다. 마케팅에 쓰지 않습니다."),
    h("h2", {}, "보관 기간"),
    h("p", {}, "상담 내용은 상담일로부터 ", F("[1년]"), " 보관 후 삭제합니다. 결제 기록은 전자상거래법에 따라 5년 보관합니다. 탈퇴·삭제 요청은 아래 이메일로 받습니다."),
    h("h2", {}, "제3자 제공·위탁"),
    h("p", {}, "결제 처리: (주)토스페이먼츠. 서버 운영: ", F("[호스팅 업체]"), ". 그 밖에는 법령에 따른 경우를 빼고 제공하지 않습니다."),
    h("h2", {}, "책임자"),
    h("p", {}, F("[이름]"), " · ", F("[이메일]")),
  )), foot());
}

boot().catch((e) => render(page(h("div", { class: "notice err" }, e.message))));
