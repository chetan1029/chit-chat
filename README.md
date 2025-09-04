# Chit-Chat

Build a REST API that can submit, fetch (new + historical), and delete messages. Must be usable with `curl` and easy to run.
---

## 🚀 Features

- Submit message
- Fetch only new message
- Delete single message
- Delete multiple messages
- Fetch all the messages

---

## 📦 Tech Stack

- **Backend**: FastAPI, SQLModel, Pydantic
- **Database**: PostgreSQL
- **DevOps**: Docker, Docker-compose

---

## 📂 To run project on localhost 
- **run**: docker-compose up

## 📂 cURL Cheatsheet

**Create**
```bash
curl -X 'POST' \
  'http://localhost:8080/messages/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "recipient": "alice@example.com",
  "content": "hello, alice!"
}'
```

**Fetch new** (marks fetched)
```bash
curl -X 'GET' \
  'http://localhost:8080/messages/new?recipient=alice%40example.com&limit=100' \
  -H 'accept: application/json'
```

**Fetch slice** (historical, incl. fetched)
```bash
curl -X 'GET' \
  'http://localhost:8080/messages/?recipient=alice@example.com&start=0&stop=50&order=asc' \
  -H 'accept: application/json'
```

**Delete single**
```bash
curl -X 'DELETE' \
  'http://localhost:8080/messages/e6196138-b5d2-4395-a2f2-7456e7704271' \
  -H 'accept: */*'
```

**Delete multiple**
```bash
curl -X 'POST' \
  'http://localhost:8080/messages/delete' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  "e6196138-b5d2-4395-a2f2-7456e7704271",
"f5b57bbb-be81-45e4-9313-297c0d223a74"
]'
```

**Health**
```bash
curl -s 'http://localhost:8080/healthcheck'
```

```bash
curl -s 'http://localhost:8080/healthcheck/db'
```

---


