// 결제 승인·취소. PAYMENT_MODE=mock 이면 실제 결제사에 연결하지 않습니다.
import { PAYMENT_MODE, TOSS_SECRET_KEY } from "./config.js";

const TOSS_API = "https://api.tosspayments.com/v1/payments";

function authHeader() {
  return "Basic " + Buffer.from(TOSS_SECRET_KEY + ":").toString("base64");
}

async function tossPost(path, body, idempotencyKey) {
  const headers = { Authorization: authHeader(), "Content-Type": "application/json" };
  if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;
  const res = await fetch(TOSS_API + path, { method: "POST", headers, body: JSON.stringify(body) });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.message || `결제사 응답 오류 (${res.status})`);
    err.code = data.code;
    throw err;
  }
  return data;
}

// 결제 승인: 이 호출이 성공해야 실제로 돈이 빠져나갑니다.
export async function confirmPayment({ paymentKey, orderId, amount }) {
  if (PAYMENT_MODE === "mock") {
    if (!paymentKey.startsWith("mock_")) throw new Error("테스트 모드에서는 테스트 결제만 가능합니다.");
    return { paymentKey, orderId, totalAmount: amount, method: "테스트" };
  }
  return tossPost("/confirm", { paymentKey, orderId, amount }, `confirm-${orderId}`);
}

// 환불 (amount 없으면 전액)
export async function cancelPayment({ paymentKey, reason, amount, idempotencyKey }) {
  if (PAYMENT_MODE === "mock" || paymentKey.startsWith("mock_")) return { status: "CANCELED" };
  const body = { cancelReason: reason };
  if (amount) body.cancelAmount = amount;
  return tossPost(`/${encodeURIComponent(paymentKey)}/cancel`, body, idempotencyKey);
}
