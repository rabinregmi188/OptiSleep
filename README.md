# OptiSleep

Sleep tracking app with a static React-via-CDN frontend and a FastAPI +
Supabase backend. Built as a portfolio piece — full-stack, real auth,
real Postgres, with Gemini-powered weekly insights coming next.

## Live

- Frontend (demo): https://optisleep-app.vercel.app/
- Listed on the portfolio: https://rabin-portfolio-rust.vercel.app/

## Repo layout

```
.
├── index.html             # frontend shell (deployed to Vercel)
├── optisleep/             # frontend JSX (compiled in-browser via Babel standalone)
├── vercel.json            # static-deploy override for Vercel
└── backend/               # FastAPI service (deployed separately)
    ├── app/               # FastAPI app, routes, auth, db
    ├── sql/               # Supabase schema + RLS policies
    ├── tests/             # pytest unit tests
    ├── Dockerfile
    └── README.md          # backend setup + endpoint docs
```

## Stack

| Layer       | Tech                                              |
|-------------|---------------------------------------------------|
| Frontend    | React 18 (via CDN) + Babel standalone, no build   |
| API         | FastAPI · Pydantic v2 · uvicorn                   |
| Auth        | Supabase Auth (HS256 JWTs verified server-side)   |
| Database    | Postgres on Supabase, with Row Level Security     |
| Insights    | Gemini API (Google AI Studio) — *coming next*     |
| Cache       | Redis (Upstash) — *coming next*                   |
| Container   | Docker, deployable to Render / Fly.io / Cloud Run |
| Tests       | pytest                                            |

## Backend setup

See [`backend/README.md`](backend/README.md) for the full walkthrough
(Supabase schema, env vars, local dev, tests, Docker).
