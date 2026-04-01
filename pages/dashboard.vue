<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

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
const bestQual = computed(() => analytics.bestQuality(sessions.value))
const avgQual = computed(() => analytics.averageQuality(sessions.value))
const comparison = computed(() => analytics.weeklyComparison(sessions.value))
const qualDist = computed(() => analytics.qualityDistribution(sessions.value))
const weeklyData = computed(() => analytics.dailyAverages(sessions.value))
const trendPoints = computed(() => analytics.trendData(sessions.value))
const insight = computed(() => analytics.generateInsight(sessions.value, streak.value))

const deltaStr = computed(() => {
  const d = comparison.value.delta
  if (d === 0) return undefined
  return (d > 0 ? '+' : '') + d + 'h'
})
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Dashboard</h1>
      <NuxtLink to="/log" class="btn-primary text-sm">+ Log Sleep</NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16 text-slate-400">
      <div class="text-4xl animate-pulse mb-3">📊</div>
      <p>Loading your sleep data...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="!sessions.length" class="card p-12 text-center">
      <div class="text-5xl mb-4">😴</div>
      <h2 class="text-xl font-bold mb-2">Welcome to OptiSleep!</h2>
      <p class="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">
        Start by logging your first sleep session. Your dashboard will come alive with charts and insights.
      </p>
      <div class="flex flex-wrap justify-center gap-3">
        <NuxtLink to="/log" class="btn-primary">Log Sleep</NuxtLink>
        <NuxtLink to="/goals" class="btn-secondary">Set a Goal</NuxtLink>
      </div>
    </div>

    <!-- Dashboard content -->
    <div v-else class="space-y-6">
      <!-- Insight banner -->
      <InsightBanner :message="insight" />

      <!-- Stat cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon="🛏️"
          label="Avg Sleep"
          :value="avgHours + 'h'"
          :delta="deltaStr"
          :delta-positive="comparison.delta >= 0"
        />
        <StatCard
          icon="🔥"
          label="Current Streak"
          :value="streak + ' days'"
        />
        <StatCard
          icon="⭐"
          label="Best Quality"
          :value="bestQual + '/5'"
        />
        <StatCard
          icon="📋"
          label="Total Sessions"
          :value="totalCount"
        />
      </div>

      <!-- Charts row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Trend chart -->
        <div class="card p-5">
          <h3 class="font-bold mb-4">Sleep Trend (30 days)</h3>
          <SleepTrendChart
            :data="trendPoints"
            :target-hours="goal?.target_hours"
          />
        </div>

        <!-- Weekly bar chart -->
        <div class="card p-5">
          <h3 class="font-bold mb-4">Daily Averages</h3>
          <WeeklyBarChart
            :data="weeklyData"
            :target-hours="goal?.target_hours"
          />
        </div>
      </div>

      <!-- Quality donut -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="card p-5">
          <h3 class="font-bold mb-4">Quality Distribution</h3>
          <QualityDonut :distribution="qualDist" :average-quality="avgQual" />
        </div>

        <!-- Quick actions -->
        <div class="lg:col-span-2 card p-5">
          <h3 class="font-bold mb-4">Quick Actions</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <NuxtLink to="/log" class="flex items-center gap-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors">
              <span class="text-2xl">😴</span>
              <div>
                <p class="font-semibold text-sm">Log Sleep</p>
                <p class="text-xs text-slate-500">Record last night</p>
              </div>
            </NuxtLink>
            <NuxtLink to="/goals" class="flex items-center gap-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors">
              <span class="text-2xl">🎯</span>
              <div>
                <p class="font-semibold text-sm">Goals</p>
                <p class="text-xs text-slate-500">{{ goal ? 'View streak' : 'Set a goal' }}</p>
              </div>
            </NuxtLink>
            <NuxtLink to="/history" class="flex items-center gap-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors">
              <span class="text-2xl">📋</span>
              <div>
                <p class="font-semibold text-sm">History</p>
                <p class="text-xs text-slate-500">All sessions</p>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
