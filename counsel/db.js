import { DatabaseSync } from "node:sqlite";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";

export function openDb(path) {
  if (path !== ":memory:") mkdirSync(dirname(path), { recursive: true });
  const db = new DatabaseSync(path);
  db.exec(`
    PRAGMA journal_mode = WAL;
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      email TEXT NOT NULL UNIQUE,
      pw_hash TEXT NOT NULL,
      nickname TEXT NOT NULL,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS auth_sessions (
      token TEXT PRIMARY KEY,
      user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
      is_admin INTEGER NOT NULL DEFAULT 0,
      expires_at TEXT NOT NULL
    );

    -- 상담사가 열어둔 시간 (UTC ISO 문자열)
    CREATE TABLE IF NOT EXISTS slots (
      starts_at TEXT PRIMARY KEY
    );

    CREATE TABLE IF NOT EXISTS bookings (
      id TEXT PRIMARY KEY,
      order_id TEXT NOT NULL UNIQUE,
      user_id TEXT NOT NULL REFERENCES users(id),
      product TEXT NOT NULL,
      amount INTEGER NOT NULL,
      starts_at TEXT NOT NULL,
      ends_at TEXT NOT NULL,
      intake TEXT NOT NULL,
      status TEXT NOT NULL,          -- pending | paid | done | noshow | canceled | expired
      payment_key TEXT,
      created_at TEXT NOT NULL,
      paid_at TEXT,
      canceled_at TEXT,
      cancel_reason TEXT,
      refunded_amount INTEGER NOT NULL DEFAULT 0
    );
    -- 같은 시간에 살아있는 예약은 하나만
    CREATE UNIQUE INDEX IF NOT EXISTS one_booking_per_slot
      ON bookings(starts_at) WHERE status IN ('pending','paid','done','noshow');
    CREATE INDEX IF NOT EXISTS bookings_user ON bookings(user_id);

    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      booking_id TEXT NOT NULL REFERENCES bookings(id),
      sender TEXT NOT NULL,           -- user | admin | system
      body TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS messages_booking ON messages(booking_id, id);
  `);
  return db;
}

export function tx(db, fn) {
  db.exec("BEGIN IMMEDIATE");
  try {
    const r = fn();
    db.exec("COMMIT");
    return r;
  } catch (e) {
    db.exec("ROLLBACK");
    throw e;
  }
}
