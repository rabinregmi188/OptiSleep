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

## Endpoints

| Method | Path                       | Auth | Description                                              |
|-------:|----------------------------|------|----------------------------------------------------------|
|   GET  | `/health`                  | no   | Liveness probe                                           |
|   GET  | `/api/sessions`            | yes  | List the caller's sleep sessions                         |
|  POST  | `/api/sessions`            | yes  | Log a new session                                        |
|  PATCH | `/api/sessions/{id}`       | yes  | Edit a session                                           |
| DELETE | `/api/sessions/{id}`       | yes  | Delete a session                                         |
|   GET  | `/api/goals`               | yes  | Get the caller's goal                                    |
|   PUT  | `/api/goals`               | yes  | Create or update goal                                    |
|   GET  | `/api/analytics/summary`   | yes  | Sleep score + streak + drift + consistency (Redis cache) |
|   GET  | `/api/insights/weekly`     | yes  | Gemini-generated coaching summary, persisted per week    |

### Analytics summary

Computed from the last 30 sessions (configurable via `?days=`):

- **sleep_score** (0–100) — weighted blend of duration vs goal (50%), self-reported quality (30%), bedtime consistency (20%)
- **avg_duration_minutes**, **avg_quality**, **avg_bedtime**
- **weekend_drift_minutes** — signed difference between weekend and weekday bedtimes
- **bedtime_consistency_minutes** — population stdev of bedtime
- **current_streak** — consecutive nights logged (counts back from today or yesterday)

Cached for 5 minutes per `(user, days)` key.

### Weekly insight

Builds a prompt from the last 14 nights' summary metrics and asks Gemini for
a 2–3 sentence personalized coaching paragraph. Lookup order:

1. Redis (1h TTL)
2. `insights` table (this week's row, keyed on Monday)
3. Compute summary → call Gemini → write to table → cache → return

Only the first request per user per week pays for a Gemini call.

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
