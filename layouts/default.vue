<script setup lang="ts">
const user = useSupabaseUser()
const client = useSupabaseClient()
const route = useRoute()
const mobileMenuOpen = ref(false)

const navLinks = [
  { to: '/dashboard', label: 'Dashboard', icon: 'grid' },
  { to: '/log', label: 'Log Sleep', icon: 'plus' },
  { to: '/goals', label: 'Goals', icon: 'target' },
  { to: '/history', label: 'History', icon: 'clock' },
]

function isActive(path: string) {
  return route.path === path
}

async function logout() {
  await client.auth.signOut()
  navigateTo('/login')
}
</script>

<template>
  <div class="opti-shell min-h-screen">
    <div class="hidden min-h-screen lg:flex">
      <aside class="flex w-[224px] shrink-0 flex-col border-r px-3 py-6" style="background: var(--surface); border-color: var(--border);">
        <NuxtLink to="/dashboard" class="mb-8 flex items-center gap-2.5 px-2">
          <span class="grid h-8 w-8 place-items-center rounded-lg" style="background: var(--accent-dim);">
            <AppIcon name="moon" :size="16" color="var(--accent)" />
          </span>
          <span class="opti-title text-[15px] font-bold">OptiSleep</span>
        </NuxtLink>

        <nav class="space-y-1">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="sidebar-link"
            :class="{ active: isActive(link.to) }"
          >
            <AppIcon :name="link.icon" :size="16" :color="isActive(link.to) ? 'var(--accent)' : 'var(--muted)'" />
            <span>{{ link.label }}</span>
          </NuxtLink>
        </nav>

        <div class="mt-auto border-t px-2 pt-4" style="border-color: var(--border);">
          <div class="flex items-center gap-2.5">
            <div class="grid h-8 w-8 place-items-center rounded-full text-xs font-bold text-white" style="background: linear-gradient(135deg,#7c3aed,#a78bfa);">
              {{ (user?.email || 'R').slice(0, 1).toUpperCase() }}
            </div>
            <div class="min-w-0">
              <p class="truncate text-sm font-semibold">{{ user?.email?.split('@')[0] || 'Rabin' }}</p>
              <p class="text-xs" style="color: var(--muted);">Sleep consistency mode</p>
            </div>
          </div>
          <button class="opti-btn-ghost mt-3 w-full justify-start text-xs" @click="logout">
            <AppIcon name="chevR" :size="14" />
            Logout
          </button>
        </div>
      </aside>

      <main class="min-h-screen flex-1 overflow-y-auto">
        <div class="mx-auto w-full max-w-[1240px] px-6 py-6">
          <slot />
        </div>
      </main>
    </div>

    <div class="min-h-screen lg:hidden">
      <header class="sticky top-0 z-40 border-b px-4 py-3 backdrop-blur" style="background: rgba(16,13,28,0.88); border-color: var(--border);">
        <div class="flex items-center justify-between">
          <NuxtLink to="/dashboard" class="flex items-center gap-2">
            <span class="grid h-8 w-8 place-items-center rounded-lg" style="background: var(--accent-dim);">
              <AppIcon name="moon" :size="15" color="var(--accent)" />
            </span>
            <span class="opti-title text-base font-bold">OptiSleep</span>
          </NuxtLink>
          <button
            class="rounded-lg border p-2"
            style="border-color: var(--border); background: var(--surface2);"
            @click="mobileMenuOpen = !mobileMenuOpen"
            aria-label="Toggle menu"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7h16M4 12h16M4 17h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div v-if="mobileMenuOpen" class="mt-3 space-y-1">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="sidebar-link"
            :class="{ active: isActive(link.to) }"
            @click="mobileMenuOpen = false"
          >
            <AppIcon :name="link.icon" :size="16" :color="isActive(link.to) ? 'var(--accent)' : 'var(--muted)'" />
            <span>{{ link.label }}</span>
          </NuxtLink>
          <button class="opti-btn-ghost w-full justify-start text-sm" @click="logout">
            <AppIcon name="chevR" :size="14" />
            Logout
          </button>
        </div>
      </header>
      <main class="mx-auto w-full max-w-[1240px] px-4 py-4">
        <slot />
      </main>
    </div>
  </div>
</template>
