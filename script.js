// 사전예약 신청을 받을 주소.
// Formspree(https://formspree.io)에서 폼을 만든 뒤 발급받은 주소를 넣으세요.
// 예: "https://formspree.io/f/abcdwxyz"
// 비어 있으면 신청 내용이 어디에도 저장되지 않습니다(테스트 모드).
const FORM_ENDPOINT = "";

const form = document.getElementById("preorder-form");
const success = document.getElementById("form-success");
const errorBox = document.getElementById("form-error");
const submitBtn = document.getElementById("submit-btn");
const mobileCta = document.querySelector(".mobile-cta");

// 개인정보 안내 펼치기
document.getElementById("privacy-toggle").addEventListener("click", () => {
  const box = document.getElementById("privacy");
  box.hidden = !box.hidden;
});

function validate() {
  const name = form.elements.name;
  const email = form.elements.email;
  const agree = form.elements.agree;
  [name, email].forEach((el) => el.classList.remove("invalid"));

  if (!name.value.trim()) {
    name.classList.add("invalid");
    name.focus();
    return "이름 또는 닉네임을 입력해 주세요.";
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    email.classList.add("invalid");
    email.focus();
    return "올바른 이메일 주소를 입력해 주세요.";
  }
  if (!agree.checked) {
    return "개인정보 수집·이용에 동의해 주세요.";
  }
  return "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = validate();
  errorBox.textContent = message;
  if (message) return;

  const data = Object.fromEntries(new FormData(form));
  data.submittedAt = new Date().toISOString();

  submitBtn.disabled = true;
  submitBtn.textContent = "신청 중…";

  try {
    if (FORM_ENDPOINT) {
      const res = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("submit failed");
    } else {
      console.warn("[테스트 모드] FORM_ENDPOINT가 비어 있어 신청 내용이 저장되지 않았습니다.", data);
    }
    form.hidden = true;
    success.hidden = false;
    success.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch {
    errorBox.textContent = "신청 중 문제가 생겼어요. 잠시 후 다시 시도해 주세요.";
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "사전예약 신청하기";
  }
});

// 공유하기
document.getElementById("share-btn").addEventListener("click", async () => {
  const shareData = {
    title: "남자끼리 하는 말",
    text: "그 사람은 왜 그랬을까? 남자들끼리만 하던 이야기, 사전예약 중이래!",
    url: location.href.split("#")[0],
  };
  if (navigator.share) {
    try { await navigator.share(shareData); } catch { /* 사용자가 취소 */ }
  } else {
    try {
      await navigator.clipboard.writeText(shareData.url);
      alert("링크가 복사됐어요! 친구에게 보내 보세요.");
    } catch {
      prompt("아래 링크를 복사해 주세요.", shareData.url);
    }
  }
});

// 스크롤 등장 효과
const revealTargets = document.querySelectorAll(".card, .quote, .chapters li, .benefits li, .faq details");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealTargets.forEach((el, i) => {
    el.classList.add("reveal");
    el.style.transitionDelay = `${(i % 4) * 80}ms`;
    io.observe(el);
  });

  // 예약 섹션이 보이면 모바일 하단 버튼 숨기기
  const preorder = document.getElementById("preorder");
  new IntersectionObserver(([entry]) => {
    mobileCta.classList.toggle("hide", entry.isIntersecting);
  }, { threshold: 0.1 }).observe(preorder);
}
