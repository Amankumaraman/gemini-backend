# Gemini Backend Clone – Kuvaka Tech

A scalable, production-ready backend system that replicates Gemini-style functionality: OTP-based authentication, chatroom management, asynchronous AI response via Redis queue, and Stripe-powered subscriptions.

Live Deployment: [https://gemini-backend-bjhb.onrender.com](https://gemini-backend-bjhb.onrender.com)
Postman Collection: *\[https://lunar-resonance-556494.postman.co/workspace/Demo~0a778c18-57ff-4c69-92c5-dfa9f196ef0b/collection/23158238-a9d823d7-5997-473b-bf1d-71c6c7c37f43?action=share&creator=23158238&active-environment=23158238-58645550-6c96-439d-8deb-29dce5d21aac]*

---

## 🚀 Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **Queue:** Redis Queue (custom)
* **Cache:** Redis
* **Payments:** Stripe (Sandbox)
* **AI API:** Groq (OpenAI-compatible)
* **Auth:** OTP + JWT

---

## ✅ Features Implemented

### 🔐 User Authentication

* OTP-based login (mocked, returned via response)
* JWT-based session management
* Password reset with OTP

### 💬 Chatroom Management

* Authenticated users can:

  * Create multiple chatrooms
  * Send messages per chatroom
  * Receive Gemini (Groq API) responses asynchronously

### ⚙️ AI Integration (Gemini via Groq)

* Prompt sent to `Groq` via Redis queue worker
* AI responses saved in DB and retrievable
* Uses OpenAI-compatible Groq API (`llama3-70b-8192`)

### 🔁 Async Queue with Redis

* Custom `push_task()` and `pop_task()` logic
* Redis-backed worker (`redis_worker.py`)
* Runs independently as a background process (deployed as Render Worker/Railway Worker)

### 💸 Subscriptions via Stripe

* Checkout integration using Stripe sandbox
* Webhook on `/webhook/stripe` to upgrade user tier
* `/subscription/status` to check current plan
* Plans:

  * **Basic (Free)** – 5 messages/day
  * **Pro (Paid)** – Unlimited

### 🚦 Rate Limiting

* Implemented via message counter for **Basic** users
* Restricts to 5 prompts/day per user (configurable via env)

### 🧠 Redis Caching

* Chatroom list cached per user (`GET /chatroom`)
* Improves dashboard loading
* TTL: 10 minutes

---

## 📁 API Endpoints

| Endpoint                  | Method | Auth | Description                          |
| ------------------------- | ------ | ---- | ------------------------------------ |
| `/auth/signup`            | POST   | ❌    | Register user (mobile only)          |
| `/auth/send-otp`          | POST   | ❌    | Generate & send OTP (in response)    |
| `/auth/verify-otp`        | POST   | ❌    | Verify OTP and receive token         |
| `/auth/forgot-password`   | POST   | ❌    | Send OTP for reset                   |
| `/auth/change-password`   | POST   | ✅    | Change password                      |
| `/user/me`                | GET    | ✅    | Get current user profile             |
| `/chatroom`               | POST   | ✅    | Create a new chatroom                |
| `/chatroom`               | GET    | ✅    | List all chatrooms (cached)          |
| `/chatroom/{id}`          | GET    | ✅    | Get single chatroom                  |
| `/chatroom/{id}/message`  | POST   | ✅    | Send a message and queue AI response |
| `/chatroom/{id}/messages` | GET    | ✅    | Fetch chatroom messages              |
| `/subscribe/pro`          | POST   | ✅    | Start Stripe checkout                |
| `/webhook/stripe`         | POST   | ❌    | Stripe event handler                 |
| `/subscription/status`    | GET    | ✅    | Get user plan status                 |
| `/chatroom/usage`         | GET    | ✅    | Daily usage stats                    |

---

## 📦 Installation & Local Setup

```bash
git clone <your-repo>
cd gemini-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### .env Example:

```env
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
STRIPE_SECRET_KEY=sk_test_...
DOMAIN=http://localhost:8000
GROQ_API_KEY=your_groq_key
BASIC_DAILY_LIMIT=5
JWT_SECRET=your_jwt_secret
```

### Run App:

```bash
uvicorn app.main:app --reload
```

### Run Worker:

```bash
python redis_worker.py
```

---

## 📬 Postman Collection

* Covers all endpoints
* Includes authentication & JWT tokens
* Organized by folders:

  * Auth
  * Chatroom
  * Messages
  * Subscriptions
  * Stripe Webhooks

---

## 🧱 Architecture

* FastAPI → REST APIs
* Redis → queue + cache
* PostgreSQL → persistent storage
* Stripe → webhook, checkout
* Worker → async processing
* JWT → secure auth layer

---

## ✨ Queue System Overview

```text
[POST /chatroom/{id}/message]
          │
       Save User Msg
          │
     push_task() ➝ Redis Queue
                      │
                redis_worker.py
                      │
       Call Groq API ➝ Save AI Msg
```

---

## 🤖 Gemini API (Groq) Integration

* Compatible with OpenAI SDK
* Uses `llama3-70b-8192` model
* Responses are delayed by worker (non-blocking)
* Delivered via background saving

---

## ✅ Assumptions & Notes

* OTPs are mocked (no SMS gateway)
* User identity = mobile number
* Stripe runs in test mode only
* AI responses are not streamed
* Webhook routes are public by design (Stripe-only access)

---

## 🧪 Testing Instructions (Postman)

1. `POST /auth/send-otp` – get OTP
2. `POST /auth/verify-otp` – get JWT token
3. Use `Bearer <token>` for all next requests
4. Create chatroom → send message
5. Poll `/chatroom/{id}/messages` to view AI response
6. Subscribe using `/subscribe/pro`
7. Verify Pro tier via `/subscription/status`

---

## 🌍 Deployment

* Backend: [Render](https://gemini-backend-bjhb.onrender.com)
* Worker: Deployed on Render (background process)
* DB: Render PostgreSQL
* Redis: Render (Cloud Redis)

---

