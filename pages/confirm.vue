<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const user = useSupabaseUser()

watch(user, (val) => {
  if (val) navigateTo('/dashboard')
}, { immediate: true })
</script>

<template>
  <div class="text-center text-white">
    <div class="text-4xl mb-4 animate-pulse">😴</div>
    <p class="text-lg">Signing you in...</p>
  </div>
</template>
