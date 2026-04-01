<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>

<template>
  <div class="card p-4 bg-gradient-to-r from-indigo-50 to-violet-50 dark:from-indigo-900/20 dark:to-violet-900/20 border-indigo-200 dark:border-indigo-800">
    <div class="flex items-center gap-3">
      <span class="text-xl flex-shrink-0">💡</span>
      <p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">{{ message }}</p>
    </div>
  </div>
</template>
