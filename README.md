# Workout & Routine API

**FastAPI backend** for user accounts, workout sessions, and custom routine planning with JWT authentication and SQLAlchemy ORM.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square)

---

## Architecture

```
┌──────────────┐  JWT Bearer   ┌─────────────────────────────────┐
│ React client │ ◄────────────►│  FastAPI (main.py)              │
│ localhost:3000│  /auth/login │  ├── /workouts                  │
└──────────────┘               │  └── /routines                  │
                               └───────────────┬─────────────────┘
                                               │
                               ┌───────────────▼─────────────────┐
                               │  SQLAlchemy + SQLite            │
                               │  Users · Workouts · Routines    │
                               └─────────────────────────────────┘
```

---

## Quick start

```bash
pip install -r requirements.txt
uvicorn main:app --port 8002 --host 127.0.0.1
```

**Browser demo:** http://localhost:8002 — auto-login as `demo` / `demo123`

| | URL |
|---|-----|
| **Web UI (demo)** | http://localhost:8002 |
| **API docs (Swagger)** | http://localhost:8002/docs |
| **Health check** | http://localhost:8002/health |

> Port **8002** avoids conflicts with other local APIs on 8000.

---

## Authentication flow

1. `POST /auth/register` or `POST /auth/login` → JWT token
2. Protected routes: `Authorization: Bearer <token>`

---

## License

MIT — see [LICENSE](LICENSE).
