# Implementation Plan

## 1. Proposed DB Schema

### Tables

#### users
- id (PK)
- email (unique)
- created_at

#### events
- id (PK)
- external_id (unique) — idempotency key
- user_id (FK → users.id)
- amount
- currency
- type (credit | debit)
- created_at

#### balances
- user_id (PK, FK → users.id)
- current_balance
- updated_at

#### payouts
- id (PK)
- user_id (FK → users.id)
- amount
- status (pending | processed | failed)
- batch_id
- created_at

### Constraints & Indexes
- UNIQUE(events.external_id)
- INDEX(events.user_id, created_at)
- INDEX(payouts.batch_id)

---

## 2. Idempotency Strategy

### Guaranteed at DB level
- `events.external_id` has a UNIQUE constraint
- Prevents duplicate ingestion even under retries

### Validated at application level
- Incoming requests require an idempotency key
- Application checks for existing event before processing

---

## 3. Endpoints & Flows

### Event ingestion
- POST /events
- Validates payload
- Inserts event atomically
- Updates user balance in same transaction

### Balance calculation
- GET /balances/{user_id}
- Reads from balances table
- No heavy recalculation per request

### Payout batch
- POST /payouts/run
- Selects eligible balances
- Creates payout records
- Marks batch_id for traceability

---

## 4. Async Payout Strategy

### Mechanism
- Async FastAPI endpoints
- DB-level locking to avoid double payouts
- Batch processing using transactions

### Limitations
- No external queue (out of scope)
- Payouts processed sequentially per batch

---

## 5. Testing Plan

### Priority tests
1. Idempotent event ingestion
2. Balance consistency after multiple events
3. Duplicate request handling
4. Payout batch integrity

### Tools
- pytest
- async test client
- isolated test database

---

## 6. Tradeoffs / Out of Scope

- No external message broker (Kafka, SQS)
- No real payment provider integration
- Focus on correctness over performance tuning
