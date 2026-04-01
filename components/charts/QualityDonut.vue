<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps<{
  distribution: number[]
  averageQuality: number
}>()

const chartData = computed(() => ({
  labels: ['Terrible', 'Poor', 'Okay', 'Good', 'Excellent'],
  datasets: [
    {
      data: props.distribution,
      backgroundColor: [
        '#EF4444',
        '#F59E0B',
        '#EAB308',
        '#84CC16',
        '#22C55E',
      ],
      borderWidth: 0,
      hoverOffset: 8,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    tooltip: {
      callbacks: {
        label: (ctx: any) => `${ctx.label}: ${ctx.raw} nights`,
      },
    },
  },
}
</script>

<template>
  <div class="relative h-48">
    <Doughnut :data="chartData" :options="options" />
    <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
      <div class="text-center">
        <p class="text-2xl font-bold">{{ averageQuality }}</p>
        <p class="text-xs text-slate-500 dark:text-slate-400">avg quality</p>
      </div>
    </div>
  </div>
</template>
