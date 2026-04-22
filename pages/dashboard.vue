<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const user = useSupabaseUser()
const { getRecentSessions, getSessionCount } = useSleepSessions()
const { getActiveGoal, calculateStreak } = useGoals()
const analytics = useAnalytics()

const sessions = ref<any[]>([])
const goal = ref<any>(null)
const streak = ref(0)
const totalCount = ref(0)
const loading = ref(true)

onMounted(async () => {
  try {
    const [recentData, goalData, count] = await Promise.all([
      getRecentSessions(30),
      getActiveGoal(),
      getSessionCount(),
    ])

    sessions.value = recentData
    goal.value = goalData
    totalCount.value = count

    if (goalData && recentData.length) {
      streak.value = await calculateStreak(recentData, goalData.target_hours)
    }
  } catch (e) {
    console.error('Failed to load dashboard:', e)
  } finally {
    loading.value = false
  }
})

const avgHours = computed(() => analytics.averageHours(sessions.value))
const avgQual = computed(() => analytics.averageQuality(sessions.value))
const comparison = computed(() => analytics.weeklyComparison(sessions.value))
const qualDist = computed(() => analytics.qualityDistribution(sessions.value))
const weeklyData = computed(() => analytics.dailyAverages(sessions.value))
const trendPoints = computed(() => analytics.trendData(sessions.value))
const insight = computed(() => analytics.generateInsight(sessions.value, streak.value))

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
})

const todayLabel = computed(() =>
  new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  }),
)

const comparisonText = computed(() => {
  const d = Math.abs(comparison.value.delta)
  if (d === 0) return 'same as last week'
  return `${d}h vs last week`
})

const qualityLegend = ['Terrible', 'Poor', 'Okay', 'Good', 'Excellent']
</script>

<template>
  <section class="fade-up space-y-5">
    <header class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <p class="opti-title text-2xl font-bold sm:text-[28px]">
          {{ greeting }}, {{ user?.email?.split('@')[0] || 'Rabin' }}
        </p>
        <p class="text-sm" style="color: var(--text-soft);">
          {{ todayLabel }} · 30-day overview
        </p>
      </div>
      <NuxtLink to="/log" class="opti-btn-primary px-5 py-2.5">
        <AppIcon name="plus" :size="14" color="white" />
        Log Sleep
      </NuxtLink>
    </header>

    <div v-if="loading" class="opti-panel rounded-2xl p-12 text-center">
      <div class="mx-auto mb-4 grid h-12 w-12 animate-pulse place-items-center rounded-xl" style="background: var(--accent-dim);">
        <AppIcon name="moon" :size="20" color="var(--accent)" />
      </div>
      <p style="color: var(--text-soft);">Loading your sleep data...</p>
    </div>

    <div v-else-if="!sessions.length" class="opti-panel rounded-2xl p-12 text-center">
      <div class="mx-auto mb-4 grid h-14 w-14 place-items-center rounded-2xl" style="background: var(--accent-dim);">
        <AppIcon name="moon" :size="24" color="var(--accent)" />
      </div>
      <h2 class="opti-title mb-1 text-2xl font-bold">Welcome to OptiSleep</h2>
      <p class="mx-auto mb-6 max-w-md text-sm leading-relaxed" style="color: var(--text-soft);">
        Start by logging your first sleep session. Your dashboard will populate with trends,
        quality patterns, and actionable insights.
      </p>
      <div class="flex flex-wrap justify-center gap-3">
        <NuxtLink to="/log" class="opti-btn-primary">Log Sleep</NuxtLink>
        <NuxtLink to="/goals" class="opti-btn-secondary">Set Goal</NuxtLink>
      </div>
    </div>

    <template v-else>
      <InsightBanner :message="insight" />

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          icon="moon"
          label="Avg Sleep"
          :value="`${avgHours}h`"
          :delta="comparisonText"
          :delta-positive="comparison.delta >= 0"
        />
        <StatCard
          icon="flame"
          label="Current Streak"
          :value="`${streak}d`"
          sub="consecutive nights"
          accent-color="var(--orange)"
        />
        <StatCard
          icon="star"
          label="Avg Quality"
          :value="`${avgQual}/5`"
          sub="out of 5"
          accent-color="var(--amber)"
        />
        <StatCard
          icon="grid"
          label="Total Sessions"
          :value="totalCount"
          sub="past 30 days"
        />
      </div>

      <div class="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <article class="opti-panel rounded-2xl p-5 xl:col-span-2">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="opti-title text-base font-bold">Sleep Trend · 30 days</h3>
            <span class="text-xs" style="color: var(--muted);">
              {{ goal?.target_hours || 8 }}h target
            </span>
          </div>
          <SleepTrendChart :data="trendPoints" :target-hours="goal?.target_hours || 8" />
        </article>

        <article class="opti-panel rounded-2xl p-5">
          <h3 class="opti-title mb-3 text-base font-bold">Quality Distribution</h3>
          <QualityDonut :distribution="qualDist" :average-quality="avgQual" />
          <div class="mt-2 space-y-1.5">
            <div
              v-for="(label, idx) in qualityLegend"
              :key="label"
              class="flex items-center justify-between text-xs"
            >
              <span style="color: var(--text-soft);">{{ label }}</span>
              <span style="color: var(--muted);">{{ qualDist[idx] }}</span>
            </div>
          </div>
        </article>
      </div>

      <div class="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <article class="opti-panel rounded-2xl p-5 xl:col-span-2">
          <h3 class="opti-title mb-4 text-base font-bold">Weekly Pattern</h3>
          <WeeklyBarChart :data="weeklyData" :target-hours="goal?.target_hours || 8" />
        </article>

        <article class="opti-panel rounded-2xl p-5">
          <h3 class="opti-title mb-4 text-base font-bold">Quick Actions</h3>
          <div class="space-y-2.5">
            <NuxtLink to="/log" class="flex items-center gap-3 rounded-xl border p-3 transition-colors hover:bg-[var(--accent-dim)]" style="border-color: var(--border);">
              <span class="grid h-8 w-8 place-items-center rounded-lg" style="background: var(--accent-dim);">
                <AppIcon name="plus" :size="14" color="var(--accent)" />
              </span>
              <div>
                <p class="text-sm font-semibold">Log Sleep</p>
                <p class="text-xs" style="color: var(--muted);">Record last night</p>
              </div>
            </NuxtLink>
            <NuxtLink to="/goals" class="flex items-center gap-3 rounded-xl border p-3 transition-colors hover:bg-[var(--accent-dim)]" style="border-color: var(--border);">
              <span class="grid h-8 w-8 place-items-center rounded-lg" style="background: var(--accent-dim);">
                <AppIcon name="target" :size="14" color="var(--accent)" />
              </span>
              <div>
                <p class="text-sm font-semibold">Goals</p>
                <p class="text-xs" style="color: var(--muted);">{{ streak }} day streak</p>
              </div>
            </NuxtLink>
            <NuxtLink to="/history" class="flex items-center gap-3 rounded-xl border p-3 transition-colors hover:bg-[var(--accent-dim)]" style="border-color: var(--border);">
              <span class="grid h-8 w-8 place-items-center rounded-lg" style="background: var(--accent-dim);">
                <AppIcon name="clock" :size="14" color="var(--accent)" />
              </span>
              <div>
                <p class="text-sm font-semibold">History</p>
                <p class="text-xs" style="color: var(--muted);">All sessions</p>
              </div>
            </NuxtLink>
          </div>
        </article>
      </div>
    </template>
  </section>
</template>
