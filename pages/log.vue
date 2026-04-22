<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { addSession } = useSleepSessions()

const form = ref({
  date: new Date().toISOString().split('T')[0],
  bedtime: '22:30',
  wakeTime: '06:30',
  quality: 4,
  notes: '',
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

const duration = computed(() => {
  const bed = new Date(`${form.value.date}T${form.value.bedtime}:00`)
  let wake = new Date(`${form.value.date}T${form.value.wakeTime}:00`)
  if (wake <= bed) wake.setDate(wake.getDate() + 1)
  const diff = (wake.getTime() - bed.getTime()) / (1000 * 60 * 60)
  return Math.round(diff * 10) / 10
})

const qualityLabels = ['Terrible', 'Poor', 'Okay', 'Good', 'Excellent']
const qualityColors = ['#f87171', '#fb923c', '#fbbf24', '#34d399', '#a78bfa']

async function handleSubmit() {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    const bedtime = new Date(`${form.value.date}T${form.value.bedtime}:00`).toISOString()
    let wakeDate = new Date(`${form.value.date}T${form.value.wakeTime}:00`)
    if (new Date(bedtime) >= wakeDate) wakeDate.setDate(wakeDate.getDate() + 1)

    await addSession({
      bedtime,
      wake_time: wakeDate.toISOString(),
      quality_rating: form.value.quality,
      notes: form.value.notes || undefined,
    })

    success.value = true
    setTimeout(() => navigateTo('/dashboard'), 1200)
  } catch (e: any) {
    error.value = e.message || 'Failed to log sleep session'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="fade-up mx-auto w-full max-w-2xl">
    <div v-if="success" class="opti-panel flex min-h-[320px] flex-col items-center justify-center rounded-3xl p-8 text-center">
      <div class="mb-4 grid h-16 w-16 place-items-center rounded-full border-2" style="border-color: var(--green); background: rgba(110,231,183,0.12);">
        <AppIcon name="check" :size="28" color="var(--green)" />
      </div>
      <h2 class="opti-title text-2xl font-bold">Sleep logged!</h2>
      <p class="mt-1 text-sm" style="color: var(--text-soft);">Redirecting to dashboard...</p>
    </div>

    <form v-else class="opti-panel space-y-6 rounded-3xl p-6 sm:p-8" @submit.prevent="handleSubmit">
      <div>
        <p class="opti-eyebrow">Quick logging</p>
        <h1 class="opti-title text-2xl font-bold">Log Sleep Session</h1>
        <p class="mt-1 text-sm" style="color: var(--text-soft);">Record how you slept last night.</p>
      </div>

      <div>
        <label for="date" class="opti-label">Date</label>
        <input id="date" v-model="form.date" type="date" class="opti-input" required>
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label for="bedtime" class="opti-label">Bedtime</label>
          <input id="bedtime" v-model="form.bedtime" type="time" class="opti-input" required>
        </div>
        <div>
          <label for="wake-time" class="opti-label">Wake Time</label>
          <input id="wake-time" v-model="form.wakeTime" type="time" class="opti-input" required>
        </div>
      </div>

      <div class="rounded-xl border px-4 py-3 text-center" style="background: var(--accent-dim); border-color: var(--border-strong);">
        <span class="text-sm" style="color: var(--text-soft);">Duration · </span>
        <span class="opti-title text-3xl font-extrabold" style="color: var(--accent);">{{ duration }}h</span>
      </div>

      <div>
        <label class="opti-label">Sleep Quality</label>
        <div class="grid grid-cols-5 gap-2">
          <button
            v-for="n in 5"
            :key="n"
            type="button"
            class="rounded-xl border px-1 py-2.5 text-center transition-all"
            :style="{
              borderColor: form.quality >= n ? qualityColors[n - 1] : 'var(--border)',
              background: form.quality >= n ? `${qualityColors[n - 1]}22` : 'transparent',
            }"
            @click="form.quality = n"
          >
            <p class="opti-title text-xl font-extrabold" :style="{ color: form.quality >= n ? qualityColors[n - 1] : 'var(--muted)' }">
              {{ n }}
            </p>
            <p class="mt-0.5 text-[9px] font-semibold uppercase tracking-[0.03em]" :style="{ color: form.quality >= n ? qualityColors[n - 1] : 'var(--muted)' }">
              {{ qualityLabels[n - 1] }}
            </p>
          </button>
        </div>
      </div>

      <div>
        <label for="notes" class="opti-label">
          Notes <span class="normal-case tracking-normal" style="color: var(--muted);">— optional</span>
        </label>
        <textarea
          id="notes"
          v-model="form.notes"
          rows="3"
          placeholder="How did you sleep? Any dreams?"
          class="opti-input resize-none"
        />
      </div>

      <p v-if="error" class="text-sm text-red-300">{{ error }}</p>

      <button type="submit" :disabled="loading" class="opti-btn-primary w-full rounded-xl py-3.5 text-base">
        <span v-if="loading">Saving...</span>
        <span v-else>Log Sleep Session</span>
      </button>
    </form>
  </section>
</template>
