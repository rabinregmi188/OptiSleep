<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const props = defineProps<{
  data: { label: string; hours: number }[]
  targetHours?: number
}>()

const chartData = computed(() => ({
  labels: props.data.map((d) => d.label),
  datasets: [
    {
      label: 'Avg Hours',
      data: props.data.map((d) => d.hours),
      backgroundColor: props.data.map((d) => {
        if (!props.targetHours) return '#6366F1'
        if (d.hours >= props.targetHours) return '#22C55E'
        if (d.hours >= props.targetHours * 0.9) return '#F59E0B'
        return '#EF4444'
      }),
      borderRadius: 8,
      barPercentage: 0.6,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      callbacks: {
        label: (ctx: any) => `${ctx.parsed.y}h avg`,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 12,
      grid: { color: 'rgba(148, 163, 184, 0.1)' },
      ticks: { callback: (v: any) => v + 'h' },
    },
    x: {
      grid: { display: false },
    },
  },
}
</script>

<template>
  <div class="h-48">
    <Bar :data="chartData" :options="options" />
  </div>
</template>
