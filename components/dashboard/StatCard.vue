<script setup lang="ts">
withDefaults(defineProps<{
  icon: string
  label: string
  value: string | number
  delta?: string
  deltaPositive?: boolean
  accentColor?: string
  sub?: string
}>(), {
  accentColor: 'var(--accent)',
})
</script>

<template>
  <article class="opti-panel rounded-2xl p-5">
    <div class="mb-3 flex items-start justify-between">
      <p class="text-[11px] font-medium uppercase tracking-[0.06em]" style="color: var(--text-soft);">
        {{ label }}
      </p>
      <span
        class="grid h-8 w-8 place-items-center rounded-[10px]"
        :style="{ background: `${accentColor}1a` }"
      >
        <AppIcon :name="icon" :size="15" :color="accentColor" />
      </span>
    </div>

    <p class="opti-title text-3xl font-extrabold leading-none">{{ value }}</p>

    <p
      v-if="delta"
      class="mt-1 text-xs font-medium"
      :style="{ color: deltaPositive ? 'var(--green)' : 'var(--red)' }"
    >
      {{ deltaPositive ? '↑' : '↓' }} {{ delta }}
    </p>
    <p v-else-if="sub" class="mt-1 text-xs" style="color: var(--text-soft);">
      {{ sub }}
    </p>
  </article>
</template>
