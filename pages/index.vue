<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const user = useSupabaseUser()

onMounted(() => {
  if (user.value) navigateTo('/dashboard')
})

const stars = Array.from({ length: 52 }, (_, i) => ({
  left: ((i * 73.137 + 11.5) % 100).toFixed(2),
  top: ((i * 47.293 + 31.7) % 100).toFixed(2),
  size: i % 6 === 0 ? 2.5 : i % 3 === 0 ? 1.5 : 1,
  opacity: (0.18 + (i % 7) * 0.04).toFixed(2),
}))

const features = [
  { icon: 'grid', title: 'Analytics', description: 'Trend charts and 30-day sleep insights.' },
  { icon: 'target', title: 'Goals & Streaks', description: 'Build lasting habits with nightly targets.' },
  { icon: 'zap', title: 'Smart Insights', description: 'Personalized recommendations from your data.' },
]
</script>

<template>
  <section class="relative mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-6xl flex-col items-center justify-center px-4 py-12 text-center text-[var(--text)]">
    <div class="pointer-events-none absolute inset-0">
      <div
        v-for="(star, idx) in stars"
        :key="idx"
        class="absolute rounded-full"
        :style="{
          left: `${star.left}%`,
          top: `${star.top}%`,
          width: `${star.size}px`,
          height: `${star.size}px`,
          background: `rgba(196,181,253,${star.opacity})`,
        }"
      />
    </div>

    <div
      class="relative mb-10 h-24 w-24 rounded-full"
      style="
        background: radial-gradient(circle at 38% 32%, #d8b4fe, #6d28d9);
        box-shadow: 0 0 60px rgba(139, 92, 246, 0.5), 0 0 120px rgba(139, 92, 246, 0.18);
        animation: floatMoon 7s ease-in-out infinite;
      "
    >
      <span class="absolute left-[54%] top-[21%] h-4 w-4 rounded-full bg-black/15" />
      <span class="absolute left-[28%] top-[57%] h-2.5 w-2.5 rounded-full bg-black/10" />
    </div>

    <h1 class="opti-title mb-6 text-5xl font-extrabold leading-[0.98] sm:text-6xl md:text-7xl">
      Sleep smarter.<br>
      <span class="gradient-title">Wake stronger.</span>
    </h1>

    <p class="mx-auto mb-10 max-w-xl text-lg leading-relaxed" style="color: var(--text-soft);">
      Track your sleep, build streaks, and understand your rest with beautiful real-time analytics.
    </p>

    <NuxtLink to="/login" class="opti-btn-primary px-9 py-3.5 text-base" style="animation: pulseGlow 3s ease-in-out infinite;">
      Get started
      <AppIcon name="arrowR" :size="18" color="white" />
    </NuxtLink>

    <div class="mt-14 grid w-full max-w-4xl gap-4 sm:grid-cols-3">
      <article
        v-for="feature in features"
        :key="feature.title"
        class="rounded-2xl border p-5 text-left backdrop-blur-md"
        style="background: rgba(255,255,255,0.025); border-color: var(--border);"
      >
        <div class="mb-3" style="color: var(--accent);">
          <AppIcon :name="feature.icon" :size="20" />
        </div>
        <h3 class="opti-title mb-1 text-base font-bold">{{ feature.title }}</h3>
        <p class="text-sm leading-relaxed" style="color: var(--text-soft);">
          {{ feature.description }}
        </p>
      </article>
    </div>
  </section>
</template>
