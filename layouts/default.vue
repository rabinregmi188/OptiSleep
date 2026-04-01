<script setup lang="ts">
const user = useSupabaseUser()
const client = useSupabaseClient()
const isDark = useState('dark', () => true)
const mobileMenuOpen = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('optisleep-dark')
  isDark.value = saved !== null ? saved === 'true' : true
  applyTheme()
})

function toggleDark() {
  isDark.value = !isDark.value
  localStorage.setItem('optisleep-dark', String(isDark.value))
  applyTheme()
}

function applyTheme() {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

async function logout() {
  await client.auth.signOut()
  navigateTo('/login')
}

const navLinks = [
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/log', label: 'Log Sleep', icon: '😴' },
  { to: '/history', label: 'History', icon: '📋' },
  { to: '/goals', label: 'Goals', icon: '🎯' },
]
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white transition-colors duration-200">
    <!-- Header -->
    <header class="sticky top-0 z-50 glass border-b border-slate-200 dark:border-slate-700">
      <nav class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/dashboard" class="flex items-center gap-2 font-bold text-lg">
          <span class="text-2xl">😴</span>
          <span class="gradient-text">OptiSleep</span>
        </NuxtLink>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-1">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="btn-ghost text-sm"
            active-class="!bg-indigo-50 dark:!bg-indigo-900/30 !text-indigo-600 dark:!text-indigo-400"
          >
            <span>{{ link.icon }}</span>
            <span>{{ link.label }}</span>
          </NuxtLink>
        </div>

        <!-- Right side -->
        <div class="flex items-center gap-3">
          <button
            @click="toggleDark"
            class="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <span v-if="isDark" class="text-lg">☀️</span>
            <span v-else class="text-lg">🌙</span>
          </button>

          <div v-if="user" class="hidden sm:flex items-center gap-2">
            <span class="text-sm text-slate-500 dark:text-slate-400">{{ user.email }}</span>
            <button @click="logout" class="btn-ghost text-sm text-red-500 hover:!bg-red-50 dark:hover:!bg-red-900/20">
              Logout
            </button>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700"
            aria-label="Toggle menu"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </nav>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 space-y-1">
        <NuxtLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="btn-ghost text-sm w-full justify-start"
          active-class="!bg-indigo-50 dark:!bg-indigo-900/30 !text-indigo-600 dark:!text-indigo-400"
          @click="mobileMenuOpen = false"
        >
          <span>{{ link.icon }}</span>
          <span>{{ link.label }}</span>
        </NuxtLink>
        <button v-if="user" @click="logout" class="btn-ghost text-sm text-red-500 w-full justify-start">
          Logout
        </button>
      </div>
    </header>

    <!-- Page content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-200 dark:border-slate-700 py-6 text-center text-sm text-slate-400 dark:text-slate-500">
      <p>&copy; 2026 Rabin Regmi &middot; Built with Nuxt.js & Supabase</p>
    </footer>
  </div>
</template>
