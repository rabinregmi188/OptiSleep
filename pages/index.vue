<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const user = useSupabaseUser()

onMounted(() => {
  if (user.value) navigateTo('/dashboard')
})
</script>

<template>
  <div class="text-center max-w-2xl mx-auto">
    <!-- Hero -->
    <div class="text-6xl sm:text-7xl mb-6">😴</div>
    <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-white leading-tight mb-4">
      Sleep Better with
      <span class="block bg-gradient-to-r from-cyan-300 to-indigo-300 bg-clip-text text-transparent">OptiSleep</span>
    </h1>
    <p class="text-lg text-white/60 max-w-lg mx-auto mb-10 leading-relaxed">
      Track your sleep patterns, set goals, build streaks, and visualize your progress with real-time analytics dashboards.
    </p>

    <!-- CTA -->
    <div class="flex flex-wrap items-center justify-center gap-4">
      <NuxtLink
        to="/login"
        class="inline-flex items-center gap-2 px-8 py-4 rounded-full font-bold text-lg bg-white text-indigo-600 hover:bg-slate-100 shadow-xl shadow-white/10 transition-all duration-200"
      >
        Get Started
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </NuxtLink>
    </div>

    <!-- Feature highlights -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-16">
      <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
        <div class="text-3xl mb-3">📊</div>
        <h3 class="font-bold text-white mb-1">Analytics</h3>
        <p class="text-sm text-white/50">Charts and insights about your sleep patterns</p>
      </div>
      <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
        <div class="text-3xl mb-3">🎯</div>
        <h3 class="font-bold text-white mb-1">Goals</h3>
        <p class="text-sm text-white/50">Set targets and track your streaks</p>
      </div>
      <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
        <div class="text-3xl mb-3">🔒</div>
        <h3 class="font-bold text-white mb-1">Secure</h3>
        <p class="text-sm text-white/50">OAuth login with row-level security</p>
      </div>
    </div>

    <!-- Footer -->
    <p class="mt-16 text-white/30 text-sm">
      Built by Rabin Regmi &middot; Nuxt.js &middot; Supabase &middot; Tailwind CSS
    </p>
  </div>
</template>
