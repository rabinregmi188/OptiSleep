# OptiSleep API

FastAPI service that powers the OptiSleep frontend. Authenticates users via
Supabase JWTs, persists sleep sessions and goals in Postgres (via Supabase),
and (in the next milestone) generates weekly insights with the Gemini API.

## Architecture

```
[Browser]  ──JWT──▶  [FastAPI]  ──┐
   │                              │   user_client(token) → Supabase REST (RLS enforced)
   │                              │   service_client()   → Supabase REST (admin, bypasses RLS)
   │                              └─▶ Gemini API     (commit 2)
   │                              └─▶ Redis cache    (commit 2)
```

## Setup

1. **Create a Supabase project** at https://supabase.com/dashboard.
2. In the SQL editor, run `sql/01_schema.sql` then `sql/02_rls.sql`.
3. From *Project Settings → API*, copy the four values into a `.env` (see `.env.example`):
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `SUPABASE_JWT_SECRET`
4. Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://localhost:8000/docs for the OpenAPI UI
```

Or with Docker:

```bash
docker compose up --build
```

## Endpoints (commit 1)

| Method | Path                     | Auth | Description                       |
|-------:|--------------------------|------|-----------------------------------|
|   GET  | `/health`                | no   | Liveness probe                    |
|   GET  | `/api/sessions`          | yes  | List the caller's sleep sessions  |
|  POST  | `/api/sessions`          | yes  | Log a new session                 |
|  PATCH | `/api/sessions/{id}`     | yes  | Edit a session                    |
| DELETE | `/api/sessions/{id}`     | yes  | Delete a session                  |
|   GET  | `/api/goals`             | yes  | Get the caller's goal             |
|   PUT  | `/api/goals`             | yes  | Create or update goal             |

Coming next:
- `GET /api/analytics/summary` — sleep score, streaks, weekend drift
- `GET /api/insights/weekly` — Gemini-generated coaching summary
- Redis caching for analytics endpoints

## Tests

```bash
pytest
```

Unit tests cover JWT verification and the health endpoint. Integration tests
(against a real Supabase project) live behind a `pytest -m integration` flag
that's added once the test project is provisioned.

## Deployment

The Dockerfile is intentionally small enough to deploy on Render, Fly.io,
Railway, or Cloud Run with no extra config. Environment variables are read
from the platform's secrets, not committed to the repo.
