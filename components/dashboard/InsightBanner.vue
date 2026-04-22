<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>

<template>
  <div
    class="fade-up flex items-start gap-3 rounded-2xl border px-4 py-3"
    style="
      background: linear-gradient(135deg, rgba(109,40,217,0.18), rgba(167,139,250,0.08));
      border-color: rgba(167,139,250,0.22);
    "
  >
    <span class="mt-0.5 grid h-7 w-7 place-items-center rounded-lg" style="background: rgba(167,139,250,0.16);">
      <AppIcon name="zap" :size="14" color="var(--accent-light)" />
    </span>
    <p class="text-sm leading-relaxed" style="color: var(--accent-light);">
      {{ message }}
    </p>
  </div>
</template>
