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
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

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
      borderColor: '#a78bfa',
      backgroundColor: 'rgba(167, 139, 250, 0.22)',
      fill: true,
      tension: 0.35,
      borderWidth: 2.5,
      pointRadius: 0,
      pointHoverRadius: 4,
      pointBackgroundColor: '#c4b5fd',
    },
    ...(props.targetHours
      ? [{
          label: 'Goal',
          data: props.data.map(() => props.targetHours),
          borderColor: 'rgba(167, 139, 250, 0.6)',
          borderDash: [5, 4],
          borderWidth: 1.5,
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
    legend: { display: false },
    tooltip: {
      backgroundColor: '#17122a',
      borderColor: 'rgba(167,139,250,0.22)',
      borderWidth: 1,
      callbacks: {
        label: (ctx: any) => `${ctx.parsed.y}h`,
      },
    },
  },
  scales: {
    y: {
      min: 4,
      max: 11,
      grid: { color: 'rgba(167, 139, 250, 0.1)' },
      ticks: {
        color: 'rgba(155, 135, 196, 0.9)',
        callback: (v: any) => `${v}h`,
      },
    },
    x: {
      grid: { display: false },
      ticks: {
        color: 'rgba(155, 135, 196, 0.7)',
        maxTicksLimit: 8,
      },
    },
  },
}
</script>

<template>
  <div class="h-52">
    <Line :data="chartData" :options="options" />
  </div>
</template>
