<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const user = useSupabaseUser()

watch(user, (val) => {
  if (val) navigateTo('/dashboard')
}, { immediate: true })
</script>

<template>
  <div class="mx-auto max-w-md rounded-3xl border p-8 text-center" style="background: rgba(16,13,28,0.82); border-color: var(--border);">
    <div class="mx-auto mb-4 grid h-14 w-14 animate-pulse place-items-center rounded-2xl" style="background: var(--accent-dim);">
      <AppIcon name="moon" :size="24" color="var(--accent)" />
    </div>
    <p class="opti-title text-2xl font-bold">Signing you in...</p>
    <p class="mt-1 text-sm" style="color: var(--text-soft);">One moment while we finish authentication.</p>
  </div>
</template>
