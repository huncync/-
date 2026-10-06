// ───────────── 설정 ─────────────
// 알림 신청을 받을 주소. Formspree(https://formspree.io)에서 폼을 만들고 받은 주소를 넣으세요.
// 예: "https://formspree.io/f/abcdwxyz"
// 비어 있으면 테스트 모드입니다 — 신청 화면은 동작하지만 내용이 어디에도 저장되지 않습니다.
const FORM_ENDPOINT = "";

// 선주문 결제 페이지 주소(자체몰·스마트스토어·텀블벅 등). 11월 11일 전까지 넣으면 됩니다.
const PAYMENT_URL = "";

// 일정 (한국 시간)
const OPEN_AT = new Date("2026-11-11T00:00:00+09:00");     // 선주문 오픈
const PRESALE_END = new Date("2026-11-18T00:00:00+09:00"); // 11/17 화요일 밤까지 → 18일 0시부터 정가
const SHIP_AT = new Date("2026-12-02T00:00:00+09:00");     // 발송

// 테스트용: 주소 끝에 ?phase=presale 또는 ?phase=regular 를 붙이면 해당 시점 화면을 미리 볼 수 있습니다.
// ────────────────────────────────

const $ = (sel) => document.querySelector(sel);

function currentPhase(now) {
  const forced = new URLSearchParams(location.search).get("phase");
  if (["before", "presale", "regular"].includes(forced)) return forced;
  if (now < OPEN_AT) return "before";
  if (now < PRESALE_END) return "presale";
  return "regular";
}

const phase = currentPhase(new Date());

// ── 시점별 화면 전환 ──
function applyPhase() {
  const heroCta = $("#hero-cta");
  const heroSub = $("#hero-sub");
  const sticky = $("#sticky-cta");
  const navCta = document.querySelector("[data-cta-label]");
  const buy = $("#buy-block");
  const buyLink = $("#buy-link");

  if (phase === "before") return; // 기본 마크업이 오픈 전 화면

  const price = phase === "presale" ? "22,000원" : "29,000원";
  const label = phase === "presale" ? `선주문하기 · ${price}` : `구매하기 · ${price}`;

  buy.hidden = false;
  $("#buy-title").textContent = label;
  $("#buy-desc").textContent = phase === "presale"
    ? "11월 17일 화요일 밤까지입니다. 18일부터 29,000원."
    : "선주문 기간이 끝나 정가로 판매합니다. 12월 2일부터 순서대로 발송됩니다.";
  buyLink.textContent = label;
  if (PAYMENT_URL) buyLink.href = PAYMENT_URL;
  else buyLink.addEventListener("click", (e) => { e.preventDefault(); alert("결제 페이지를 준비하고 있습니다. 아래에 이메일을 남겨 주시면 열리는 대로 알려드립니다."); });

  heroCta.textContent = label;
  heroCta.href = "#reserve";
  heroSub.textContent = phase === "presale"
    ? "선주문하시면 1장 전문을 바로 보내드립니다. 전권은 12월 2일 발송."
    : "PDF로 보내드립니다. 받으신 뒤 7일 안에는 이유를 묻지 않고 환불해 드립니다.";
  sticky.textContent = label;
  navCta.textContent = phase === "presale" ? "선주문" : "구매";

  $("#form-title").textContent = "이메일만 남겨 두셔도 됩니다";
  $("#form-desc").textContent = "결제는 하지 않습니다. 새 소식과 남은 기간 안내만 이메일로 보내드립니다.";
  $("#submit-btn").textContent = "소식 받기";
}

// ── 카운트다운 ──
function startCountdown() {
  const box = $("#countdown");
  const label = $("#launch-label");
  const target = phase === "before" ? OPEN_AT : phase === "presale" ? PRESALE_END : null;

  if (!target) {
    box.classList.add("hidden");
    label.textContent = new Date() < SHIP_AT ? "12월 2일 수요일 발송" : "지금 바로 받아보실 수 있습니다";
    return;
  }
  label.textContent = phase === "before" ? "선주문 오픈까지" : "선주문가 마감까지";

  const els = { d: box.querySelector("[data-d]"), h: box.querySelector("[data-h]"), m: box.querySelector("[data-m]"), s: box.querySelector("[data-s]") };
  const pad = (n) => String(n).padStart(2, "0");
  const tick = () => {
    let diff = Math.max(0, target - Date.now());
    if (diff === 0) { location.reload(); return; }
    const d = Math.floor(diff / 86400000); diff -= d * 86400000;
    const h = Math.floor(diff / 3600000); diff -= h * 3600000;
    const m = Math.floor(diff / 60000); diff -= m * 60000;
    const s = Math.floor(diff / 1000);
    els.d.textContent = d; els.h.textContent = pad(h); els.m.textContent = pad(m); els.s.textContent = pad(s);
  };
  tick();
  setInterval(tick, 1000);
}

// ── 일정 표시 ──
function markTimeline() {
  const items = [...document.querySelectorAll("#timeline li")];
  const nowMs = phase === "before" ? Date.now()
    : phase === "presale" ? Math.max(Date.now(), OPEN_AT.getTime())
    : Math.max(Date.now(), PRESALE_END.getTime());
  let current = 0;
  items.forEach((li, i) => {
    if (new Date(li.dataset.from + "T00:00:00+09:00").getTime() <= nowMs) current = i;
  });
  items.forEach((li, i) => li.classList.add(i < current ? "past" : i === current ? "current" : "future"));
}

// ── 분기 카드 → 신청서 상황 미리 선택 ──
document.querySelectorAll(".card.pick").forEach((card) => {
  card.addEventListener("click", () => {
    const radio = document.querySelector(`#part-seg input[value="${card.dataset.part}"]`);
    if (radio) radio.checked = true;
    $("#reserve").scrollIntoView({ behavior: "smooth" });
  });
});

// ── 약관 펼치기 ──
document.querySelectorAll("[data-toggle]").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault(); // 라벨 안의 버튼이라 체크박스가 같이 눌리지 않게
    const box = document.getElementById(btn.dataset.toggle);
    box.hidden = !box.hidden;
    btn.textContent = box.hidden ? "내용 보기" : "접기";
  });
});

// ── 신청서 ──
const form = $("#reserve-form");
const errorBox = $("#form-error");
const submitBtn = $("#submit-btn");

function validate() {
  const email = form.elements.email;
  email.classList.remove("invalid");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) {
    email.classList.add("invalid");
    email.focus();
    return "이메일 주소를 다시 확인해 주십시오.";
  }
  if (!form.elements.agree_privacy.checked) return "개인정보 수집·이용에 동의해 주셔야 신청이 됩니다.";
  if (!form.elements.agree_marketing.checked) return "선주문 안내 메일 수신에 동의해 주셔야 오픈 소식을 보내드릴 수 있습니다.";
  return "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = validate();
  errorBox.textContent = message;
  if (message) return;

  const fd = new FormData(form);
  const data = {
    email: fd.get("email").trim(),
    name: (fd.get("name") || "").trim(),
    part: fd.get("part") || "",
    situation: (fd.get("situation") || "").trim(),
    read: fd.get("read") || "",
    agree_privacy: "동의",
    agree_marketing: "동의",
    consent_at: new Date().toISOString(), // 수신동의 증빙용
    phase,
    source: new URLSearchParams(location.search).get("utm_source") || document.referrer || "direct",
    _subject: "[말이 줄어든 다음] 선주문 알림 신청",
  };

  const original = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = "보내는 중…";

  try {
    if (FORM_ENDPOINT) {
      const res = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
    } else {
      console.warn("[테스트 모드] FORM_ENDPOINT가 비어 있어 신청 내용이 저장되지 않았습니다.", data);
    }
    form.hidden = true;
    $("#buy-block").hidden = true;
    $("#done").hidden = false;
    $("#reserve").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    errorBox.textContent = "보내는 중에 문제가 생겼습니다. 잠시 뒤 다시 눌러 주십시오.";
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = original;
  }
});

// ── 공유 ──
$("#share-btn").addEventListener("click", async () => {
  const url = location.origin + location.pathname;
  const shareData = { title: "말이 줄어든 다음 — 남자들끼리 하는 말 3권", text: "2권은 거기서 멈췄고, 3권은 거기서 시작한대.", url };
  if (navigator.share) {
    try { await navigator.share(shareData); } catch { /* 취소 */ }
    return;
  }
  try {
    await navigator.clipboard.writeText(url);
    alert("링크를 복사했습니다.");
  } catch {
    prompt("아래 링크를 복사해 주십시오.", url);
  }
});

// ── 모바일 하단 버튼: 신청 구간에서는 숨김 ──
if ("IntersectionObserver" in window) {
  const sticky = $("#sticky-cta");
  const visible = new Set();
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => (en.isIntersecting ? visible.add(en.target) : visible.delete(en.target)));
    sticky.classList.toggle("hide", visible.size > 0);
  }, { threshold: 0.05 });
  io.observe($("#launch"));
  io.observe($("#hero-cta"));
  io.observe($("#reserve"));
}

applyPhase();
startCountdown();
markTimeline();

// ── 스크롤 등장 효과 ──
if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const targets = document.querySelectorAll(".card, .quote, .excerpt, .toc-part, .gate li, .price-card, .terms, .benefits li, .faq details");
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  targets.forEach((el, i) => {
    el.classList.add("reveal");
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    io.observe(el);
  });
}
