<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { getSessions, deleteSession } = useSleepSessions()

const sessions = ref<any[]>([])
const loading = ref(true)
const deleting = ref<string | null>(null)

onMounted(async () => {
  try {
    sessions.value = await getSessions(100)
  } catch (e) {
    console.error('Failed to load sessions:', e)
  } finally {
    loading.value = false
  }
})

async function handleDelete(id: string) {
  if (!confirm('Delete this sleep session?')) return
  deleting.value = id
  try {
    await deleteSession(id)
    sessions.value = sessions.value.filter((s) => s.id !== id)
  } catch (e) {
    console.error('Failed to delete:', e)
  } finally {
    deleting.value = null
  }
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  })
}

function formatTime(dateStr: string) {
  return new Date(dateStr).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  })
}

function durationHours(minutes: number) {
  return Math.round((minutes / 60) * 10) / 10
}

const qualityLabels = ['Terrible', 'Poor', 'Okay', 'Good', 'Excellent']
const qualityColors = ['#f87171', '#fb923c', '#fbbf24', '#34d399', '#a78bfa']
</script>

<template>
  <section class="fade-up space-y-4">
    <header class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="opti-title text-2xl font-bold">Sleep History</h1>
        <p class="text-sm" style="color: var(--text-soft);">
          {{ sessions.length }} sessions recorded
        </p>
      </div>
      <NuxtLink to="/log" class="opti-btn-primary px-5 py-2.5">
        <AppIcon name="plus" :size="14" color="white" />
        Log Sleep
      </NuxtLink>
    </header>

    <div v-if="loading" class="opti-panel rounded-2xl p-12 text-center">
      <div class="mx-auto mb-4 grid h-12 w-12 animate-pulse place-items-center rounded-xl" style="background: var(--accent-dim);">
        <AppIcon name="clock" :size="20" color="var(--accent)" />
      </div>
      <p style="color: var(--text-soft);">Loading sessions...</p>
    </div>

    <div v-else-if="!sessions.length" class="opti-panel rounded-2xl p-12 text-center">
      <div class="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-xl" style="background: var(--accent-dim);">
        <AppIcon name="clock" :size="20" color="var(--accent)" />
      </div>
      <h2 class="opti-title text-xl font-bold">No sleep sessions yet</h2>
      <p class="mx-auto mt-1 max-w-md text-sm" style="color: var(--text-soft);">
        Start tracking your sleep to unlock patterns and consistency insights.
      </p>
      <NuxtLink to="/log" class="opti-btn-primary mt-5">Log Your First Night</NuxtLink>
    </div>

    <div v-else class="space-y-2.5">
      <article
        v-for="session in sessions"
        :key="session.id"
        class="opti-panel flex items-start gap-4 rounded-2xl border-l-[3px] px-4 py-3.5"
        :style="{ borderLeftColor: qualityColors[session.quality_rating - 1] }"
      >
        <div class="w-9 shrink-0 text-center">
          <p class="opti-title text-2xl font-extrabold leading-none" :style="{ color: qualityColors[session.quality_rating - 1] }">
            {{ session.quality_rating }}
          </p>
          <p class="text-[10px]" style="color: var(--muted);">/5</p>
        </div>

        <div class="mt-0.5 h-9 w-px shrink-0" style="background: var(--border);" />

        <div class="min-w-0 flex-1">
          <div class="mb-1 flex flex-wrap items-center gap-2">
            <p class="text-sm font-semibold">{{ formatDate(session.bedtime) }}</p>
            <span class="rounded-full px-2 py-0.5 text-[11px] font-semibold" style="background: var(--accent-dim); color: var(--accent);">
              {{ durationHours(session.duration_minutes) }}h
            </span>
            <span class="text-[11px] font-semibold" :style="{ color: qualityColors[session.quality_rating - 1] }">
              {{ qualityLabels[session.quality_rating - 1] }}
            </span>
          </div>
          <p class="text-sm" style="color: var(--text-soft);">
            {{ formatTime(session.bedtime) }} → {{ formatTime(session.wake_time) }}
            <span v-if="session.notes" style="color: var(--muted);"> · {{ session.notes }}</span>
          </p>
        </div>

        <button
          class="rounded-lg p-2 transition-colors"
          :disabled="deleting === session.id"
          style="color: var(--muted);"
          @click="handleDelete(session.id)"
        >
          <AppIcon name="trash" :size="14" />
        </button>
      </article>
    </div>
  </section>
</template>
