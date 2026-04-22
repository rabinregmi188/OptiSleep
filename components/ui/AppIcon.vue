<script setup lang="ts">
withDefaults(defineProps<{
  name: string
  size?: number
  color?: string
  strokeWidth?: number
}>(), {
  size: 20,
  color: 'currentColor',
  strokeWidth: 1.75,
})
</script>

<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" aria-hidden="true">
    <template v-if="name === 'moon'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </template>
    <template v-else-if="name === 'grid'">
      <rect :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" x="3" y="3" width="7" height="7" rx="1.5" />
      <rect :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" x="14" y="3" width="7" height="7" rx="1.5" />
      <rect :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" x="3" y="14" width="7" height="7" rx="1.5" />
      <rect :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" x="14" y="14" width="7" height="7" rx="1.5" />
    </template>
    <template v-else-if="name === 'plus'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M12 5v14M5 12h14" />
    </template>
    <template v-else-if="name === 'target'">
      <circle :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" cx="12" cy="12" r="9" />
      <circle :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" cx="12" cy="12" r="4.5" />
      <circle cx="12" cy="12" r="2" :fill="color" />
    </template>
    <template v-else-if="name === 'clock'">
      <circle :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" cx="12" cy="12" r="9" />
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M12 7v5l3.5 2" />
    </template>
    <template v-else-if="name === 'flame'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M12 2s-5 5.5-5 10a5 5 0 0 0 10 0c0-3-2-5-2-5s-1 3.5-3 3.5S10 9 10 8c0 0 2 2.5 4.5.5C16 7 16 4 12 2z" />
    </template>
    <template v-else-if="name === 'star'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
    </template>
    <template v-else-if="name === 'trash'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M3 6h18M19 6l-1.5 14H6.5L5 6M9 6V4h6v2" />
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M10 11v5M14 11v5" />
    </template>
    <template v-else-if="name === 'arrowR'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
    </template>
    <template v-else-if="name === 'check'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M20 6L9 17l-5-5" />
    </template>
    <template v-else-if="name === 'zap'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M13 2L3 14h9l-1 8 10-12h-9z" />
    </template>
    <template v-else-if="name === 'chevR'">
      <path :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" stroke-linejoin="round" d="M9 18l6-6-6-6" />
    </template>
  </svg>
</template>
