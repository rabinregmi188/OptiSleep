<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { getActiveGoal, createGoal, updateGoal, calculateStreak } = useGoals()
const { getRecentSessions } = useSleepSessions()

const goal = ref<any>(null)
const streak = ref(0)
const loading = ref(true)
const saving = ref(false)
const editing = ref(false)

const form = ref({
  target_hours: 8,
  target_bedtime: '22:30',
  target_wake_time: '06:30',
})

onMounted(async () => {
  try {
    goal.value = await getActiveGoal()
    if (goal.value) {
      form.value.target_hours = goal.value.target_hours
      form.value.target_bedtime = goal.value.target_bedtime || '22:30'
      form.value.target_wake_time = goal.value.target_wake_time || '06:30'

      const sessions = await getRecentSessions(60)
      streak.value = await calculateStreak(sessions, goal.value.target_hours)
    }
  } catch (e) {
    console.error('Failed to load goal:', e)
  } finally {
    loading.value = false
  }
})

const streakBest = computed(() => Math.max(goal.value?.longest_streak || 0, 30))
const streakProgress = computed(() => Math.min(100, Math.round((streak.value / streakBest.value) * 100)))
const monthlyScore = computed(() => Math.min(100, Math.round((streak.value / 30) * 100)))

async function handleSave() {
  saving.value = true
  try {
    if (goal.value && editing.value) {
      goal.value = await updateGoal(goal.value.id, {
        target_hours: form.value.target_hours,
        target_bedtime: form.value.target_bedtime,
        target_wake_time: form.value.target_wake_time,
      })
    } else {
      goal.value = await createGoal({
        target_hours: form.value.target_hours,
        target_bedtime: form.value.target_bedtime,
        target_wake_time: form.value.target_wake_time,
      })
    }
    editing.value = false
  } catch (e) {
    console.error('Failed to save goal:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="fade-up mx-auto w-full max-w-4xl">
    <div v-if="loading" class="opti-panel rounded-2xl p-12 text-center">
      <div class="mx-auto mb-4 grid h-12 w-12 animate-pulse place-items-center rounded-xl" style="background: var(--accent-dim);">
        <AppIcon name="target" :size="20" color="var(--accent)" />
      </div>
      <p style="color: var(--text-soft);">Loading goals...</p>
    </div>

    <template v-else>
      <div v-if="goal && !editing" class="space-y-4">
        <article class="opti-panel rounded-3xl p-6 sm:p-8">
          <div class="grid items-center gap-8 md:grid-cols-[180px,1fr]">
            <div class="relative mx-auto h-44 w-44">
              <div
                class="absolute inset-0 rounded-full"
                :style="{
                  background: `conic-gradient(#a78bfa ${streakProgress}%, rgba(167,139,250,0.12) ${streakProgress}% 100%)`,
                }"
              />
              <div class="absolute inset-[12px] grid place-items-center rounded-full" style="background: var(--surface);">
                <div class="text-center">
                  <p class="opti-title text-5xl font-extrabold leading-none">{{ streak }}</p>
                  <p class="text-xs uppercase tracking-[0.08em]" style="color: var(--text-soft);">day streak</p>
                </div>
              </div>
            </div>

            <div>
              <p class="opti-title text-2xl font-bold">You&apos;re on a roll</p>
              <p class="mt-2 text-sm leading-relaxed" style="color: var(--text-soft);">
                {{ streak }} consecutive nights near your {{ goal.target_hours }}h target. Keep your bedtime
                routine stable to beat your best of {{ goal.longest_streak }} days.
              </p>

              <div class="mt-4 grid grid-cols-3 gap-2.5">
                <div class="rounded-xl border p-3 text-center" style="background: var(--surface2); border-color: var(--border);">
                  <p class="opti-title text-2xl font-extrabold" style="color: var(--accent);">{{ streak }}</p>
                  <p class="text-[11px]" style="color: var(--text-soft);">Current</p>
                </div>
                <div class="rounded-xl border p-3 text-center" style="background: var(--surface2); border-color: var(--border);">
                  <p class="opti-title text-2xl font-extrabold" style="color: var(--amber);">{{ goal.longest_streak }}</p>
                  <p class="text-[11px]" style="color: var(--text-soft);">Best</p>
                </div>
                <div class="rounded-xl border p-3 text-center" style="background: var(--surface2); border-color: var(--border);">
                  <p class="opti-title text-2xl font-extrabold" style="color: var(--green);">{{ monthlyScore }}%</p>
                  <p class="text-[11px]" style="color: var(--text-soft);">Monthly</p>
                </div>
              </div>
            </div>
          </div>
        </article>

        <article class="opti-panel rounded-3xl p-6 sm:p-8">
          <div class="mb-5 flex items-center justify-between">
            <h2 class="opti-title text-xl font-bold">Current Goal</h2>
            <button class="opti-btn-ghost" @click="editing = true">
              Edit
            </button>
          </div>

          <div class="grid gap-3 sm:grid-cols-3">
            <div class="rounded-xl border p-4 text-center" style="background: var(--surface2); border-color: var(--border);">
              <p class="opti-title text-3xl font-extrabold">{{ goal.target_hours }}h</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.06em]" style="color: var(--text-soft);">Target</p>
            </div>
            <div class="rounded-xl border p-4 text-center" style="background: var(--surface2); border-color: var(--border);">
              <p class="opti-title text-3xl font-extrabold">{{ goal.target_bedtime || '--:--' }}</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.06em]" style="color: var(--text-soft);">Bedtime</p>
            </div>
            <div class="rounded-xl border p-4 text-center" style="background: var(--surface2); border-color: var(--border);">
              <p class="opti-title text-3xl font-extrabold">{{ goal.target_wake_time || '--:--' }}</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.06em]" style="color: var(--text-soft);">Wake Up</p>
            </div>
          </div>
        </article>
      </div>

      <form v-else class="opti-panel rounded-3xl p-6 sm:p-8" @submit.prevent="handleSave">
        <div class="mb-6">
          <p class="opti-eyebrow">Goal planning</p>
          <h1 class="opti-title text-2xl font-bold">
            {{ goal ? 'Edit Goal' : 'Set Your Sleep Goal' }}
          </h1>
        </div>

        <div class="space-y-5">
          <div>
            <label for="target-hours" class="opti-label">Target Hours</label>
            <input
              id="target-hours"
              v-model.number="form.target_hours"
              type="number"
              min="4"
              max="12"
              step="0.5"
              class="opti-input"
              required
            >
          </div>

          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label for="target-bedtime" class="opti-label">Target Bedtime</label>
              <input id="target-bedtime" v-model="form.target_bedtime" type="time" class="opti-input">
            </div>
            <div>
              <label for="target-wake" class="opti-label">Target Wake Time</label>
              <input id="target-wake" v-model="form.target_wake_time" type="time" class="opti-input">
            </div>
          </div>
        </div>

        <div class="mt-6 flex flex-wrap gap-3">
          <button type="submit" :disabled="saving" class="opti-btn-primary">
            {{ saving ? 'Saving...' : (goal ? 'Update Goal' : 'Set Goal') }}
          </button>
          <button v-if="editing" type="button" class="opti-btn-secondary" @click="editing = false">
            Cancel
          </button>
        </div>
      </form>
    </template>
  </section>
</template>
