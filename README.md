# OptiSleep

Full-stack sleep tracking app with OAuth authentication, session logging, goal streaks, and real-time analytics dashboards.

## Tech Stack

- **Nuxt.js 3** - Vue 3 framework with SSG
- **Supabase** - Auth (OAuth) + PostgreSQL database + Realtime
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Analytics visualizations
- **Netlify** - Deployment

## Features

- **OAuth Login** - Sign in with GitHub or Google
- **Sleep Logging** - Record bedtime, wake time, quality rating, and notes
- **Analytics Dashboard** - Sleep trend charts, weekly averages, quality distribution
- **Goal Tracking** - Set sleep targets and track streaks
- **Dark Mode** - Full dark/light theme support
- **Row-Level Security** - Each user only sees their own data

## Setup

1. Create a [Supabase](https://supabase.com) project
2. Run `supabase-schema.sql` in the Supabase SQL Editor
3. Enable GitHub and Google OAuth providers in Supabase Auth settings
4. Copy `.env.example` to `.env` and fill in your Supabase credentials
5. Install dependencies and run:

```bash
npm install
npm run dev
```

## Deployment

Deployed on Netlify. See `netlify.toml` for build configuration.

## License

MIT
