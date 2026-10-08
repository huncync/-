// ───────────── 운영 설정 ─────────────
// 상품·가격·규칙은 여기서 바꿉니다. 바꾼 뒤 서버를 다시 켜면 반영됩니다.

export const PRODUCTS = {
  chat30: { name: "30분 채팅 상담", minutes: 30, price: 30000, desc: "한 가지 상황을 정리하고, 지금 할 것과 하지 말 것을 정합니다." },
  chat60: { name: "60분 채팅 상담", minutes: 60, price: 55000, desc: "지난 흐름부터 같이 보고, 보낼 문장까지 함께 다듬습니다." },
};

export const RULES = {
  enterBeforeMin: 10,       // 상담 시작 몇 분 전부터 채팅방에 들어갈 수 있는지
  bookAheadMinHours: 3,     // 지금으로부터 최소 몇 시간 뒤 시간부터 예약 가능
  bookAheadDays: 14,        // 며칠 뒤까지 예약 가능
  freeCancelHours: 24,      // 시작 몇 시간 전까지 고객이 직접 취소하면 전액 환불
  holdMinutes: 15,          // 결제 중인 시간을 다른 사람이 못 잡게 막아두는 시간
  slotHours: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], // 관리자 화면에 보이는 시간대(한국 시간)
};

export const TZ = "Asia/Seoul";

// ───────────── 환경 변수 ─────────────
const env = process.env;
export const PORT = Number(env.PORT || 3000);
export const BASE_URL = (env.BASE_URL || `http://localhost:${PORT}`).replace(/\/$/, "");
export const ADMIN_PASSWORD = env.ADMIN_PASSWORD || "";
export const PAYMENT_MODE = env.PAYMENT_MODE === "toss" ? "toss" : "mock";
export const TOSS_CLIENT_KEY = env.TOSS_CLIENT_KEY || "test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm";
export const TOSS_SECRET_KEY = env.TOSS_SECRET_KEY || "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6";
export const DB_PATH = env.DB_PATH || "./data/counsel.db";
export const TELEGRAM_BOT_TOKEN = env.TELEGRAM_BOT_TOKEN || "";
export const TELEGRAM_CHAT_ID = env.TELEGRAM_CHAT_ID || "";
export const SECURE_COOKIES = BASE_URL.startsWith("https://");
