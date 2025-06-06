## ✅ Features

| Feature              | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| Modular Routers   | Organized under `/api`, cleanly separated.                         |
| SQLAlchemy ORM    | Includes models for `Book`, `AuditLog`.                            |
| CRUD APIs         | Create, Read, Update, Delete for `Book` (tenant-aware).            |
| Multi-Tenancy     | Resolved via `X-Tenant-ID` header → connects to correct DB.        |
| Chatbot Hook      | OpenAI/agent-ready lifecycle integration.                          |
| Audit Log (Event) | Auto logs to persit after inserts via event listeners.             |
| JWT Auth Skeleton | `jwt.py`, `jwt_auth.py`, `auth_api.py` ready for token-based auth. |
| Middlewares       | Easy to add logging/auth/performance profiling.                    |

## 🚀 Quick Start

Install Python 3 and pip3 (If not already installed) in your machine.

### 1. Clone the Repo

```
git clone <repo-url>
cd openai-fastapi
```

### 2. Cerate VENV

```
python3 -m venv venv
source venv/bin/activate
deactivate
```

### 3. Install Dependencies

```
pip3 install -r requirements.txt
```

### 4. Update requirements (opt)

```
pip3 freeze > requirements.txt
```

### 5. Database migration (if added)

```
alembic init alembic
alembic revision --autogenerate -m "related message"
alembic upgrade head
```

### 6. Start Server

```
python3 -m app.main

[ OR ]

uvicorn app.main:app --reload --port 9001

[ OR ]

docker compose up --build -d
docker compose down
docker ps
docker logs fast_openai
```

### 7. API Docs

After running application, navigate to `/redoc`, can download & import to postman!
