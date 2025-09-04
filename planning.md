# Plan & Tech Stack

**Goal:** Build a REST API that can submit, fetch (new + historical), and delete messages. Must be usable with `curl` and easy to run.

**Stack**
- API: **FastAPI**
- ORM/Models: **SQLModel** (Pydantic v2 + SQLAlchemy 2)
- DB: **PostgreSQL**
- Runtime: **Docker** + **docker-compose**

**Why these choices?**
- Fast to build and test, great OpenAPI docs at `/docs`.
- SQLModel gives typed models with minimal boilerplate.
- Postgres supports transactional fetch with `FOR UPDATE SKIP LOCKED` (concurrency-safe “fetch new”).
- Docker-compose makes the reviewer's life easy.

---

# API Surface

## 1) Submit message
- **POST** `/messages`
- **Body**: `{ recipient: string, content: string, sender?: string }`
- **Resp**: Message object

## 2) Fetch new messages only
- **GET** `/messages/new?recipient=<id>&limit=<N>`
- Returns messages with `fetched_at IS NULL` for that recipient, **marks them fetched atomically**.

## 3) Delete single message
- **DELETE** `/messages/{id}` → 204

## 4) Delete multiple messages
- **POST** `/messages/delete` with `{ ids: UUID[] }` → `{ deleted: number }`

## 5) Fetch all messages
- **GET** `/messages?recipient=<id>&start=0&stop=50&order=asc|desc`
- Sorted by `created_at`, returns slice `[start, stop)`.

---

# Data Model

```ts
Message {
  id: UUID (pk)
  recipient: string (idx)
  content: text
  created_at: timestamptz (idx, default now())
  fetched_at?: timestamptz (idx) // null = not fetched yet
}
```

**Assumptions**
- One logical consumer per `recipient`. “Fetched” means delivered once for that recipient. (Multiple clients fetching for the same recipient will not redeliver thanks to SKIP LOCKED.)
- Plain text only; no attachments.
- No auth.
- Fetch all message act as a readonly so we are not going to mark new messages as fetched while calling fetch all messages

---

# Running Locally

```bash
docker compose up --build
# API → http://localhost:8080
# Docs → http://localhost:8080/docs
```

**Config**
- `DATABASE_URL` (set in `docker-compose.yml`). Defaults to Postgres container.

---

# cURL Cheatsheet

**Create**
```bash
curl -s -X POST 'http://localhost:8080/messages' \
  -H 'Content-Type: application/json' \
  -d '{"recipient":"alice@example.com","content":"hello, alice!"}'
```

**Fetch new** (marks fetched)
```bash
curl -s 'http://localhost:8080/messages/new?recipient=alice@example.com&limit=100'
```

**Fetch slice** (historical, incl. fetched)
```bash
curl -s 'http://localhost:8080/messages?recipient=alice@example.com&start=0&stop=50&order=asc'
```

**Delete single**
```bash
curl -i -X DELETE 'http://localhost:8080/messages/{uuid}'
```

**Delete multiple**
```bash
curl -s -X POST 'http://localhost:8080/messages/delete' \
  -H 'Content-Type: application/json' \
  -d '{"ids":["uuid-1","uuid-2"]}'
```

**Health**
```bash
curl -s 'http://localhost:8080/healthcheck'
```

---
