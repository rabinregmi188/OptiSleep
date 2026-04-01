export interface Goal {
  id: string
  user_id: string
  target_hours: number
  target_bedtime: string | null
  target_wake_time: string | null
  is_active: boolean
  current_streak: number
  longest_streak: number
  created_at: string
  updated_at: string
}

export function useGoals() {
  const client = useSupabaseClient()
  const user = useSupabaseUser()

  async function getActiveGoal() {
    const { data, error } = await client
      .from('goals')
      .select('*')
      .eq('user_id', user.value!.id)
      .eq('is_active', true)
      .maybeSingle()

    if (error) throw error
    return data as Goal | null
  }

  async function createGoal(goal: {
    target_hours: number
    target_bedtime?: string
    target_wake_time?: string
  }) {
    // Deactivate existing goals
    await client
      .from('goals')
      .update({ is_active: false })
      .eq('user_id', user.value!.id)
      .eq('is_active', true)

    const { data, error } = await client
      .from('goals')
      .insert({
        user_id: user.value!.id,
        ...goal,
      })
      .select()
      .single()

    if (error) throw error
    return data as Goal
  }

  async function updateGoal(id: string, updates: Partial<Goal>) {
    const { data, error } = await client
      .from('goals')
      .update({ ...updates, updated_at: new Date().toISOString() })
      .eq('id', id)
      .eq('user_id', user.value!.id)
      .select()
      .single()

    if (error) throw error
    return data as Goal
  }

  async function calculateStreak(sessions: { bedtime: string; duration_minutes: number }[], targetHours: number) {
    let streak = 0
    const sorted = [...sessions].sort((a, b) => new Date(b.bedtime).getTime() - new Date(a.bedtime).getTime())

    const today = new Date()
    today.setHours(0, 0, 0, 0)

    for (let i = 0; i < sorted.length; i++) {
      const sessionDate = new Date(sorted[i].bedtime)
      sessionDate.setHours(0, 0, 0, 0)

      const expectedDate = new Date(today)
      expectedDate.setDate(expectedDate.getDate() - i)

      if (sessionDate.getTime() !== expectedDate.getTime()) break

      const hours = sorted[i].duration_minutes / 60
      if (hours >= targetHours * 0.9) {
        streak++
      } else {
        break
      }
    }

    return streak
  }

  return { getActiveGoal, createGoal, updateGoal, calculateStreak }
}
