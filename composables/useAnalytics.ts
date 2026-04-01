import type { SleepSession } from './useSleepSessions'

export function useAnalytics() {
  function averageHours(sessions: SleepSession[]) {
    if (!sessions.length) return 0
    const total = sessions.reduce((sum, s) => sum + s.duration_minutes, 0)
    return Math.round((total / sessions.length / 60) * 10) / 10
  }

  function bestQuality(sessions: SleepSession[]) {
    if (!sessions.length) return 0
    return Math.max(...sessions.map((s) => s.quality_rating))
  }

  function averageQuality(sessions: SleepSession[]) {
    if (!sessions.length) return 0
    const total = sessions.reduce((sum, s) => sum + s.quality_rating, 0)
    return Math.round((total / sessions.length) * 10) / 10
  }

  function weeklyComparison(sessions: SleepSession[]) {
    const now = new Date()
    const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
    const twoWeeksAgo = new Date(now.getTime() - 14 * 24 * 60 * 60 * 1000)

    const thisWeek = sessions.filter((s) => new Date(s.bedtime) >= oneWeekAgo)
    const lastWeek = sessions.filter((s) => {
      const d = new Date(s.bedtime)
      return d >= twoWeeksAgo && d < oneWeekAgo
    })

    const thisAvg = averageHours(thisWeek)
    const lastAvg = averageHours(lastWeek)
    const delta = Math.round((thisAvg - lastAvg) * 10) / 10

    return { thisWeekAvg: thisAvg, lastWeekAvg: lastAvg, delta }
  }

  function qualityDistribution(sessions: SleepSession[]) {
    const dist = [0, 0, 0, 0, 0]
    sessions.forEach((s) => {
      if (s.quality_rating >= 1 && s.quality_rating <= 5) {
        dist[s.quality_rating - 1]++
      }
    })
    return dist
  }

  function dailyAverages(sessions: SleepSession[]) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const totals = Array(7).fill(0)
    const counts = Array(7).fill(0)

    sessions.forEach((s) => {
      const day = new Date(s.bedtime).getDay()
      totals[day] += s.duration_minutes / 60
      counts[day]++
    })

    return days.map((label, i) => ({
      label,
      hours: counts[i] ? Math.round((totals[i] / counts[i]) * 10) / 10 : 0,
    }))
  }

  function trendData(sessions: SleepSession[]) {
    return sessions.map((s) => ({
      date: new Date(s.bedtime).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      hours: Math.round((s.duration_minutes / 60) * 10) / 10,
      quality: s.quality_rating,
    }))
  }

  function generateInsight(sessions: SleepSession[], streak: number) {
    const comparison = weeklyComparison(sessions)
    const parts: string[] = []

    if (comparison.thisWeekAvg > 0) {
      parts.push(`You averaged ${comparison.thisWeekAvg}h of sleep this week`)
      if (comparison.delta > 0) {
        parts[0] += `, up ${comparison.delta}h from last week`
      } else if (comparison.delta < 0) {
        parts[0] += `, down ${Math.abs(comparison.delta)}h from last week`
      }
      parts[0] += '.'
    }

    if (streak >= 7) {
      parts.push(`Amazing ${streak}-day streak! Keep it up!`)
    } else if (streak >= 3) {
      parts.push(`Nice ${streak}-day streak going!`)
    }

    return parts.join(' ') || 'Start logging your sleep to see insights here.'
  }

  return {
    averageHours,
    bestQuality,
    averageQuality,
    weeklyComparison,
    qualityDistribution,
    dailyAverages,
    trendData,
    generateInsight,
  }
}
