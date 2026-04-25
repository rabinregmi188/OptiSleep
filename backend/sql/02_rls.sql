-- Row Level Security: every row is private to its owner.
-- The FastAPI backend authenticates the user, then forwards the access token
-- to PostgREST so these policies are enforced by Postgres itself.

alter table public.sleep_sessions enable row level security;
alter table public.goals          enable row level security;
alter table public.insights       enable row level security;

drop policy if exists "sessions_select_own" on public.sleep_sessions;
drop policy if exists "sessions_insert_own" on public.sleep_sessions;
drop policy if exists "sessions_update_own" on public.sleep_sessions;
drop policy if exists "sessions_delete_own" on public.sleep_sessions;

create policy "sessions_select_own" on public.sleep_sessions for select using (auth.uid() = user_id);
create policy "sessions_insert_own" on public.sleep_sessions for insert with check (auth.uid() = user_id);
create policy "sessions_update_own" on public.sleep_sessions for update using (auth.uid() = user_id);
create policy "sessions_delete_own" on public.sleep_sessions for delete using (auth.uid() = user_id);

drop policy if exists "goals_select_own" on public.goals;
drop policy if exists "goals_upsert_own" on public.goals;
drop policy if exists "goals_update_own" on public.goals;

create policy "goals_select_own" on public.goals for select using (auth.uid() = user_id);
create policy "goals_upsert_own" on public.goals for insert with check (auth.uid() = user_id);
create policy "goals_update_own" on public.goals for update using (auth.uid() = user_id);

drop policy if exists "insights_select_own" on public.insights;
drop policy if exists "insights_insert_service" on public.insights;

create policy "insights_select_own" on public.insights for select using (auth.uid() = user_id);
-- Insights are written by the backend using the service role, which bypasses RLS,
-- so this insert policy intentionally only allows the user themselves as a fallback.
create policy "insights_insert_service" on public.insights for insert with check (auth.uid() = user_id);
