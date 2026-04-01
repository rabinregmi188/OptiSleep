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
  <div class="max-w-lg mx-auto">
    <h1 class="text-2xl font-bold mb-6">Sleep Goals</h1>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12 text-slate-400">
      <div class="text-3xl animate-pulse mb-2">🎯</div>
      <p>Loading goals...</p>
    </div>

    <template v-else>
      <!-- Active goal display -->
      <div v-if="goal && !editing" class="space-y-4">
        <!-- Streak card -->
        <div class="card p-6 text-center bg-gradient-to-br from-indigo-500 to-violet-600 border-0 text-white">
          <div class="text-5xl mb-2">🔥</div>
          <p class="text-4xl font-extrabold">{{ streak }}</p>
          <p class="text-white/70 text-sm">day streak</p>
        </div>

        <!-- Goal details -->
        <div class="card p-6 space-y-4">
          <div class="flex items-center justify-between">
            <h2 class="font-bold text-lg">Current Goal</h2>
            <button @click="editing = true" class="btn-ghost text-sm text-indigo-500">Edit</button>
          </div>

          <div class="grid grid-cols-3 gap-3">
            <div class="text-center p-3 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
              <p class="text-2xl font-bold text-indigo-500">{{ goal.target_hours }}h</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">Target</p>
            </div>
            <div class="text-center p-3 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
              <p class="text-lg font-bold">{{ goal.target_bedtime || '--' }}</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">Bedtime</p>
            </div>
            <div class="text-center p-3 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
              <p class="text-lg font-bold">{{ goal.target_wake_time || '--' }}</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">Wake Up</p>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm text-slate-500 dark:text-slate-400 pt-2 border-t border-slate-100 dark:border-slate-700">
            <span>Longest streak: <strong class="text-slate-700 dark:text-slate-200">{{ goal.longest_streak }} days</strong></span>
          </div>
        </div>
      </div>

      <!-- Goal form (create or edit) -->
      <form v-else @submit.prevent="handleSave" class="card p-6 space-y-5">
        <h2 class="font-bold text-lg">{{ goal ? 'Edit Goal' : 'Set Your Sleep Goal' }}</h2>

        <div>
          <label for="target-hours" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Target Hours of Sleep
          </label>
          <input
            id="target-hours"
            v-model.number="form.target_hours"
            type="number"
            min="4"
            max="12"
            step="0.5"
            class="input-field"
            required
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="goal-bedtime" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Target Bedtime</label>
            <input id="goal-bedtime" v-model="form.target_bedtime" type="time" class="input-field" />
          </div>
          <div>
            <label for="goal-wake" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Target Wake Time</label>
            <input id="goal-wake" v-model="form.target_wake_time" type="time" class="input-field" />
          </div>
        </div>

        <div class="flex gap-3">
          <button type="submit" :disabled="saving" class="btn-primary flex-1 py-3">
            {{ saving ? 'Saving...' : (goal ? 'Update Goal' : 'Set Goal') }}
          </button>
          <button v-if="editing" type="button" @click="editing = false" class="btn-secondary flex-1 py-3">
            Cancel
          </button>
        </div>
      </form>
    </template>
  </div>
</template>
