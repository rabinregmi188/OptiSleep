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
    hour: 'numeric',
    minute: '2-digit',
  })
}

function durationHours(minutes: number) {
  return Math.round((minutes / 60) * 10) / 10
}

const qualityEmojis = ['😫', '😔', '😐', '😊', '😍']
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Sleep History</h1>
      <NuxtLink to="/log" class="btn-primary text-sm">+ Log Sleep</NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12 text-slate-400">
      <div class="text-3xl animate-pulse mb-2">😴</div>
      <p>Loading sessions...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="!sessions.length" class="card p-12 text-center">
      <div class="text-4xl mb-3">📋</div>
      <p class="text-lg font-semibold mb-2">No sleep sessions yet</p>
      <p class="text-slate-500 mb-4">Start tracking your sleep to see your history.</p>
      <NuxtLink to="/log" class="btn-primary">Log Your First Night</NuxtLink>
    </div>

    <!-- Session list -->
    <div v-else class="space-y-3">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="card p-4 flex items-center gap-4"
      >
        <!-- Quality emoji -->
        <div class="text-3xl flex-shrink-0">{{ qualityEmojis[session.quality_rating - 1] }}</div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <span class="font-semibold">{{ formatDate(session.bedtime) }}</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 font-mono">
              {{ durationHours(session.duration_minutes) }}h
            </span>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">
            {{ formatTime(session.bedtime) }} &rarr; {{ formatTime(session.wake_time) }}
          </p>
          <p v-if="session.notes" class="text-sm text-slate-400 dark:text-slate-500 truncate mt-1">
            {{ session.notes }}
          </p>
        </div>

        <!-- Quality stars -->
        <div class="hidden sm:flex items-center gap-0.5 flex-shrink-0">
          <span v-for="n in 5" :key="n" class="text-sm">
            {{ n <= session.quality_rating ? '⭐' : '☆' }}
          </span>
        </div>

        <!-- Delete -->
        <button
          @click="handleDelete(session.id)"
          :disabled="deleting === session.id"
          class="flex-shrink-0 p-2 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          aria-label="Delete session"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
