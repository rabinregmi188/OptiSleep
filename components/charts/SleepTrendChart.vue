<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip)

const props = defineProps<{
  data: { date: string; hours: number }[]
  targetHours?: number
}>()

const chartData = computed(() => ({
  labels: props.data.map((d) => d.date),
  datasets: [
    {
      label: 'Hours Slept',
      data: props.data.map((d) => d.hours),
      borderColor: '#6366F1',
      backgroundColor: 'rgba(99, 102, 241, 0.1)',
      fill: true,
      tension: 0.3,
      pointRadius: 4,
      pointBackgroundColor: '#6366F1',
    },
    ...(props.targetHours
      ? [{
          label: 'Goal',
          data: props.data.map(() => props.targetHours),
          borderColor: 'rgba(6, 182, 212, 0.5)',
          borderDash: [5, 5],
          pointRadius: 0,
          fill: false,
        }]
      : []),
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      callbacks: {
        label: (ctx: any) => `${ctx.parsed.y}h`,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: false,
      min: 0,
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
  <div class="h-64">
    <Line :data="chartData" :options="options" />
  </div>
</template>
