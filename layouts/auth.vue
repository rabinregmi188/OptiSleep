<template>
  <div class="auth-shell flex min-h-screen items-center justify-center px-4 py-10">
    <div class="pointer-events-none absolute inset-0 opacity-70">
      <div class="absolute -left-12 top-12 h-56 w-56 rounded-full blur-3xl" style="background: rgba(124,58,237,0.32);" />
      <div class="absolute -right-12 bottom-8 h-64 w-64 rounded-full blur-3xl" style="background: rgba(167,139,250,0.22);" />
    </div>
    <div class="relative z-10 w-full">
      <slot />
    </div>
  </div>
</template>
