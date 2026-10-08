// 예약 → 결제 → 채팅 → 취소까지 한 바퀴 (모의 결제, 메모리 DB)
import { test, before, after } from "node:test";
import assert from "node:assert/strict";

process.env.ADMIN_PASSWORD = "test-admin-pw";
process.env.PAYMENT_MODE = "mock";
const { createApp } = await import("../server.js");

const HOUR = 3600_000;
let clock = Date.parse("2026-10-08T00:00:00Z"); // 한국 시간 10/8 09:00
const app = createApp({ dbPath: ":memory:", now: () => clock });
let server, base;

before(async () => {
  server = app.listen(0);
  await new Promise((r) => server.once("listening", r));
  base = `http://127.0.0.1:${server.address().port}`;
});
after(() => server.close());

function client() {
  let cookie = "";
  return async (path, { method = "GET", body } = {}) => {
    const res = await fetch(base + path, {
      method, body: body && JSON.stringify(body),
      headers: { ...(body && { "Content-Type": "application/json" }), ...(cookie && { Cookie: cookie }) },
    });
    const set = res.headers.getSetCookie();
    if (set.length) cookie = [cookie, ...set.map((c) => c.split(";")[0])].filter(Boolean).join("; ");
    return { status: res.status, data: await res.json() };
  };
}

const admin = client();
const alice = client();
const bob = client();
const slotA = "2026-10-09T11:00:00.000Z"; // 10/9 20:00 KST
const slotB = "2026-10-09T12:00:00.000Z";
const goodBooking = { product: "chat30", intake: "헤어진 지 2주 됐고 다시 연락해도 될지 궁금합니다.", agreeTerms: true, agreeSensitive: true, agreeCrisis: true };

test("관리자만 시간을 열 수 있다", async () => {
  assert.equal((await alice("/api/admin/slots", { method: "PUT", body: { items: [] } })).status, 401);
  assert.equal((await admin("/api/admin/login", { method: "POST", body: { password: "wrong" } })).status, 401);
  assert.equal((await admin("/api/admin/login", { method: "POST", body: { password: "test-admin-pw" } })).status, 200);
  const r = await admin("/api/admin/slots", { method: "PUT", body: { items: [{ startsAt: slotA, open: true }, { startsAt: slotB, open: true }] } });
  assert.equal(r.status, 200);
  assert.deepEqual((await alice("/api/slots")).data.slots, [slotA, slotB]);
});

test("가입·로그인", async () => {
  assert.equal((await alice("/api/bookings", { method: "POST", body: { ...goodBooking, startsAt: slotA } })).status, 401);
  assert.equal((await alice("/api/signup", { method: "POST", body: { email: "a@x.com", password: "short", nickname: "a" } })).status, 400);
  assert.equal((await alice("/api/signup", { method: "POST", body: { email: "A@x.com", password: "password1", nickname: "앨리스" } })).status, 200);
  assert.equal((await bob("/api/signup", { method: "POST", body: { email: "a@x.com", password: "password1", nickname: "b" } })).status, 409);
  assert.equal((await bob("/api/signup", { method: "POST", body: { email: "b@x.com", password: "password2", nickname: "밥" } })).status, 200);
  assert.equal((await alice("/api/me")).data.user.email, "a@x.com");
});

let order, bookingId;
test("임시 예약은 시간을 잡아 두고, 동의·사연이 없으면 거절", async () => {
  assert.equal((await alice("/api/bookings", { method: "POST", body: { ...goodBooking, agreeCrisis: false, startsAt: slotA } })).status, 400);
  assert.equal((await alice("/api/bookings", { method: "POST", body: { ...goodBooking, intake: "짧음", startsAt: slotA } })).status, 400);
  const r = await alice("/api/bookings", { method: "POST", body: { ...goodBooking, startsAt: slotA } });
  assert.equal(r.status, 200);
  order = r.data; bookingId = r.data.bookingId;
  assert.equal(order.amount, 30000);
  assert.deepEqual((await bob("/api/slots")).data.slots, [slotB]);
  assert.equal((await bob("/api/bookings", { method: "POST", body: { ...goodBooking, startsAt: slotA } })).status, 409);
});

test("결제 승인: 금액 위조·남의 주문은 거절, 정상 승인은 한 번만", async () => {
  assert.equal((await alice("/api/payments/confirm", { method: "POST", body: { paymentKey: "mock_1", orderId: order.orderId, amount: 100 } })).status, 400);
  assert.equal((await bob("/api/payments/confirm", { method: "POST", body: { paymentKey: "mock_1", orderId: order.orderId, amount: 30000 } })).status, 404);
  const r = await alice("/api/payments/confirm", { method: "POST", body: { paymentKey: "mock_1", orderId: order.orderId, amount: 30000 } });
  assert.equal(r.status, 200);
  assert.equal(r.data.booking.status, "paid");
  const again = await alice("/api/payments/confirm", { method: "POST", body: { paymentKey: "mock_1", orderId: order.orderId, amount: 30000 } });
  assert.equal(again.status, 200);
  assert.equal((await alice("/api/bookings")).data.bookings.length, 1);
  assert.equal((await bob(`/api/bookings/${bookingId}`)).status, 404);
});

test("채팅은 시작 10분 전부터 끝날 때까지만", async () => {
  const send = (c, body) => c(`/api/bookings/${bookingId}/messages`, { method: "POST", body: { body } });
  assert.equal((await send(alice, "안녕하세요")).status, 403);
  clock = Date.parse(slotA) - 9 * 60_000;
  assert.equal((await send(alice, "안녕하세요")).status, 200);
  assert.equal((await admin(`/api/admin/bookings/${bookingId}/messages`, { method: "POST", body: { body: "반갑습니다" } })).status, 200);
  const room = await alice(`/api/bookings/${bookingId}`);
  assert.deepEqual(room.data.messages.map((m) => m.sender), ["system", "user", "admin"]);
  clock = Date.parse(slotA) + 31 * 60_000;
  assert.equal((await send(alice, "더 할 말")).status, 403);
  clock = Date.parse("2026-10-08T00:00:00Z");
});

test("결제창에 15분 넘게 머물면 시간이 풀리고, 늦은 승인은 다시 잡을 수 있을 때만", async () => {
  const r = await bob("/api/bookings", { method: "POST", body: { ...goodBooking, startsAt: slotB } });
  clock += 16 * 60_000;
  assert.deepEqual((await alice("/api/slots")).data.slots, [slotB]);
  const ok = await bob("/api/payments/confirm", { method: "POST", body: { paymentKey: "mock_2", orderId: r.data.orderId, amount: 30000 } });
  assert.equal(ok.status, 200);
  assert.deepEqual((await alice("/api/slots")).data.slots, []);
});

test("24시간 전까지 고객 취소 → 환불, 시간이 다시 열림", async () => {
  const r = await alice(`/api/bookings/${bookingId}/cancel`, { method: "POST" });
  assert.equal(r.status, 200);
  assert.equal(r.data.booking.status, "canceled");
  assert.equal(r.data.booking.refundedAmount, 30000);
  assert.deepEqual((await bob("/api/slots")).data.slots, [slotA]);
});

test("24시간 이내에는 고객이 직접 취소 못 하고, 관리자는 부분 환불 가능", async () => {
  const { data } = await admin("/api/admin/bookings");
  const bobs = data.bookings.find((b) => b.nickname === "밥");
  clock = Date.parse(slotB) - 2 * HOUR;
  assert.equal((await bob(`/api/bookings/${bobs.id}/cancel`, { method: "POST" })).status, 403);
  assert.equal((await admin(`/api/admin/bookings/${bobs.id}/refund`, { method: "POST", body: { amount: 99999 } })).status, 400);
  assert.equal((await admin(`/api/admin/bookings/${bobs.id}/refund`, { method: "POST", body: { amount: 15000, reason: "부분" } })).status, 200);
  const after = (await bob(`/api/bookings/${bobs.id}`)).data.booking;
  assert.equal(after.status, "canceled");
  assert.equal(after.refundedAmount, 15000);
});
