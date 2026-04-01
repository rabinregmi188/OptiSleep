<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { addSession } = useSleepSessions()

const form = ref({
  date: new Date().toISOString().split('T')[0],
  bedtime: '22:30',
  wakeTime: '06:30',
  quality: 3,
  notes: '',
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

const duration = computed(() => {
  const bed = new Date(`${form.value.date}T${form.value.bedtime}:00`)
  let wake = new Date(`${form.value.date}T${form.value.wakeTime}:00`)
  // If wake time is before bedtime, it's the next day
  if (wake <= bed) wake.setDate(wake.getDate() + 1)
  const diff = (wake.getTime() - bed.getTime()) / (1000 * 60 * 60)
  return Math.round(diff * 10) / 10
})

async function handleSubmit() {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    const bedtime = new Date(`${form.value.date}T${form.value.bedtime}:00`).toISOString()
    let wakeDate = new Date(`${form.value.date}T${form.value.wakeTime}:00`)
    if (new Date(bedtime) >= wakeDate) wakeDate.setDate(wakeDate.getDate() + 1)
    const wake_time = wakeDate.toISOString()

    await addSession({
      bedtime,
      wake_time,
      quality_rating: form.value.quality,
      notes: form.value.notes || undefined,
    })

    success.value = true
    setTimeout(() => navigateTo('/dashboard'), 1500)
  } catch (e: any) {
    error.value = e.message || 'Failed to log sleep session'
  } finally {
    loading.value = false
  }
}

const qualityLabels = ['Terrible', 'Poor', 'Okay', 'Good', 'Excellent']
</script>

<template>
  <div class="max-w-lg mx-auto">
    <h1 class="text-2xl font-bold mb-6">Log Sleep Session</h1>

    <div v-if="success" class="card p-6 text-center">
      <div class="text-4xl mb-3">✅</div>
      <p class="text-lg font-semibold text-green-600 dark:text-green-400">Sleep logged!</p>
      <p class="text-sm text-slate-500 mt-1">Redirecting to dashboard...</p>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="card p-6 space-y-5">
      <!-- Date -->
      <div>
        <label for="date" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Date</label>
        <input id="date" v-model="form.date" type="date" class="input-field" required />
      </div>

      <!-- Bedtime & Wake time row -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="bedtime" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Bedtime</label>
          <input id="bedtime" v-model="form.bedtime" type="time" class="input-field" required />
        </div>
        <div>
          <label for="waketime" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Wake Time</label>
          <input id="waketime" v-model="form.wakeTime" type="time" class="input-field" required />
        </div>
      </div>

      <!-- Duration display -->
      <div class="text-center py-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl">
        <span class="text-sm text-slate-500 dark:text-slate-400">Duration: </span>
        <span class="font-bold text-indigo-600 dark:text-indigo-400 text-lg">{{ duration }}h</span>
      </div>

      <!-- Quality rating -->
      <div>
        <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Sleep Quality</label>
        <div class="flex items-center justify-between gap-2">
          <button
            v-for="n in 5"
            :key="n"
            type="button"
            @click="form.quality = n"
            class="flex-1 py-3 rounded-xl text-center text-2xl transition-all duration-200 border-2"
            :class="form.quality >= n
              ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/30 scale-105'
              : 'border-slate-200 dark:border-slate-600 hover:border-slate-300'"
          >
            {{ n <= 2 ? '🌙' : n <= 4 ? '⭐' : '🌟' }}
            <div class="text-[10px] font-medium text-slate-500 dark:text-slate-400 mt-1">{{ qualityLabels[n - 1] }}</div>
          </button>
        </div>
      </div>

      <!-- Notes -->
      <div>
        <label for="notes" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Notes (optional)</label>
        <textarea
          id="notes"
          v-model="form.notes"
          rows="3"
          placeholder="How did you sleep? Any dreams?"
          class="input-field resize-none"
        ></textarea>
      </div>

      <!-- Error -->
      <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>

      <!-- Submit -->
      <button type="submit" :disabled="loading" class="btn-primary w-full py-4 text-base">
        <span v-if="loading">Saving...</span>
        <span v-else>Log Sleep Session</span>
      </button>
    </form>
  </div>
</template>
