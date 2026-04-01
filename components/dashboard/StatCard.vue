<script setup lang="ts">
defineProps<{
  icon: string
  label: string
  value: string | number
  delta?: string
  deltaPositive?: boolean
}>()
</script>

<template>
  <div class="card p-5">
    <div class="flex items-start justify-between">
      <span class="text-2xl">{{ icon }}</span>
      <span
        v-if="delta"
        class="text-xs font-semibold px-2 py-0.5 rounded-full"
        :class="deltaPositive ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'"
      >
        {{ delta }}
      </span>
    </div>
    <p class="text-2xl font-extrabold mt-2">{{ value }}</p>
    <p class="text-sm text-slate-500 dark:text-slate-400">{{ label }}</p>
  </div>
</template>
