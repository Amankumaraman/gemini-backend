# 🌟 Gemini Backend Clone – FastAPI + Redis Queue + Stripe + Groq AI

This project is a backend clone inspired by Google Gemini, built with **FastAPI**, **Redis-based task queue**, **GROQ's OpenAI-compatible API**, and **Stripe for subscriptions**.

## 🚀 Live Deployment

- **Backend URL**: [Render](https://gemini-backend-bjhb.onrender.com)
- **Postman Collection URL**: [Postman](https://lunar-resonance-556494.postman.co/workspace/Demo~0a778c18-57ff-4c69-92c5-dfa9f196ef0b/collection/23158238-a9d823d7-5997-473b-bf1d-71c6c7c37f43?action=share&creator=23158238)

---

## 🧩 Features

✅ OTP-based user authentication  
✅ Create and manage chatrooms  
✅ Send messages to chatrooms  
✅ Get AI (Groq) responses asynchronously  
✅ Redis queue for background processing  
✅ Stripe-based Pro subscription  
✅ Daily prompt limit for Basic users  
✅ PostgreSQL database (Supabase)  
✅ Full chat history API  
✅ Deployment-ready for Render/Railway

---

## ⚙️ Tech Stack

| Layer         | Tool                     |
|---------------|--------------------------|
| Framework     | FastAPI                  |
| Database      | PostgreSQL (via Supabase)|
| Auth          | OTP-based (mobile/email) |
| AI API        | Groq (OpenAI-compatible) |
| Queue         | Redis (custom worker)    |
| Payments      | Stripe (Subscriptions)   |
| Deployment    | Render (backend + dummy worker) |
| Rate Limiting | Redis-based daily limit  |

---

---

## 📦 Installation & Running Locally

1. **Clone the repo**

```bash
git clone https://github.com/Amankumaraman/gemini-backend.git
cd gemini-backend
````

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up `.env`**

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://localhost:6379
GROQ_API_KEY=your-groq-api-key
STRIPE_SECRET_KEY=your-stripe-secret-key
DOMAIN=http://localhost:8000
BASIC_DAILY_LIMIT=5
```

5. **Run the FastAPI server**

```bash
uvicorn main:app --reload
```

6. **Run the Redis worker (separate terminal)**

```bash
python redis_worker.py
```

---

## 🔁 Stripe Subscription Flow

* `POST /subscribe/pro` → returns Stripe Checkout URL
* After payment, Stripe sends webhook to `/webhook/stripe`
* Server upgrades user's plan to `Pro`
* `GET /subscribe/status` confirms current subscription tier

---

## 📬 Key Endpoints

| Method | Endpoint                  | Description                         |
| ------ | ------------------------- | ----------------------------------- |
| POST   | `/auth/send-otp`          | Send OTP to user                    |
| POST   | `/auth/verify-otp`        | Verify OTP and login                |
| GET    | `/chatroom/`              | Get all user chatrooms              |
| POST   | `/chatroom/`              | Create new chatroom                 |
| POST   | `/chatroom/{id}/message`  | Send message (queues Groq AI reply) |
| GET    | `/chatroom/{id}/messages` | Fetch chat history                  |
| GET    | `/chatroom/usage`         | See daily usage (Basic users)       |
| POST   | `/subscribe/pro`          | Start Stripe checkout               |
| GET    | `/subscribe/status`       | View current plan                   |
| POST   | `/webhook/stripe`         | Stripe webhook handler              |

---

## 🧠 AI Response Queue (Redis Worker)

* Messages are saved immediately.
* AI response is queued to Redis → Worker pulls → Calls Groq → Saves reply.

### Worker Entry: `redis_worker.py`

```bash
python redis_worker.py
```

Runs an async loop that pulls from Redis and processes the task via `handle_groq_task`.

---



