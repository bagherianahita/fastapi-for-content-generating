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
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

---

## Authentication flow

1. `POST /auth/register` or `POST /auth/login` → JWT token
2. Protected routes: `Authorization: Bearer <token>`

---

## License

MIT — see [LICENSE](LICENSE).
