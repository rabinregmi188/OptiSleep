-- OptiSleep schema. Run this once in the Supabase SQL Editor for a fresh project.
-- Depends on Supabase's built-in `auth.users` table.

create table if not exists public.sleep_sessions (
  id               uuid primary key default gen_random_uuid(),
  user_id          uuid not null references auth.users(id) on delete cascade,
  date             date not null,
  bedtime          time not null,
  wake_time        time not null,
  duration_minutes int  not null check (duration_minutes between 0 and 1440),
  quality_score    int  not null check (quality_score between 1 and 5),
  notes            text,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  unique (user_id, date)
);

create index if not exists sleep_sessions_user_date_idx
  on public.sleep_sessions (user_id, date desc);

create table if not exists public.goals (
  user_id                 uuid primary key references auth.users(id) on delete cascade,
  target_bedtime          time not null default '23:00',
  target_duration_minutes int  not null default 480 check (target_duration_minutes between 0 and 1440),
  weekly_target_nights    int  not null default 7   check (weekly_target_nights between 1 and 7),
  created_at              timestamptz not null default now(),
  updated_at              timestamptz not null default now()
);

create table if not exists public.insights (
  id                uuid primary key default gen_random_uuid(),
  user_id           uuid not null references auth.users(id) on delete cascade,
  week_start        date not null,
  insight_text      text not null,
  metrics_snapshot  jsonb not null,
  created_at        timestamptz not null default now(),
  unique (user_id, week_start)
);

-- updated_at triggers
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists sleep_sessions_touch on public.sleep_sessions;
create trigger sleep_sessions_touch
  before update on public.sleep_sessions
  for each row execute function public.touch_updated_at();

drop trigger if exists goals_touch on public.goals;
create trigger goals_touch
  before update on public.goals
  for each row execute function public.touch_updated_at();
