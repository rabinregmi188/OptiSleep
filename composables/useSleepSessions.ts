export interface SleepSession {
  id: string
  user_id: string
  bedtime: string
  wake_time: string
  duration_minutes: number
  quality_rating: number
  notes: string | null
  created_at: string
}

export function useSleepSessions() {
  const client = useSupabaseClient()
  const user = useSupabaseUser()

  async function getSessions(limit = 50, offset = 0) {
    const { data, error } = await client
      .from('sleep_sessions')
      .select('*')
      .eq('user_id', user.value!.id)
      .order('bedtime', { ascending: false })
      .range(offset, offset + limit - 1)

    if (error) throw error
    return data as SleepSession[]
  }

  async function getRecentSessions(days = 30) {
    const since = new Date()
    since.setDate(since.getDate() - days)

    const { data, error } = await client
      .from('sleep_sessions')
      .select('*')
      .eq('user_id', user.value!.id)
      .gte('bedtime', since.toISOString())
      .order('bedtime', { ascending: true })

    if (error) throw error
    return data as SleepSession[]
  }

  async function addSession(session: {
    bedtime: string
    wake_time: string
    quality_rating: number
    notes?: string
  }) {
    const { data, error } = await client
      .from('sleep_sessions')
      .insert({
        user_id: user.value!.id,
        ...session,
      })
      .select()
      .single()

    if (error) throw error
    return data as SleepSession
  }

  async function updateSession(id: string, updates: Partial<SleepSession>) {
    const { data, error } = await client
      .from('sleep_sessions')
      .update(updates)
      .eq('id', id)
      .eq('user_id', user.value!.id)
      .select()
      .single()

    if (error) throw error
    return data as SleepSession
  }

  async function deleteSession(id: string) {
    const { error } = await client
      .from('sleep_sessions')
      .delete()
      .eq('id', id)
      .eq('user_id', user.value!.id)

    if (error) throw error
  }

  async function getSessionCount() {
    const { count, error } = await client
      .from('sleep_sessions')
      .select('*', { count: 'exact', head: true })
      .eq('user_id', user.value!.id)

    if (error) throw error
    return count ?? 0
  }

  return { getSessions, getRecentSessions, addSession, updateSession, deleteSession, getSessionCount }
}
