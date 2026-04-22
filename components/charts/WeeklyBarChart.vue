<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

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
        if (!props.targetHours) return '#a78bfa'
        if (d.hours >= props.targetHours) return '#34d399'
        if (d.hours >= props.targetHours * 0.9) return '#fbbf24'
        return '#f87171'
      }),
      borderRadius: 12,
      barPercentage: 0.55,
      categoryPercentage: 0.75,
    },
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
        label: (ctx: any) => `${ctx.parsed.y}h avg`,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 11,
      grid: { color: 'rgba(167, 139, 250, 0.08)' },
      ticks: {
        color: 'rgba(155, 135, 196, 0.85)',
        callback: (v: any) => `${v}h`,
      },
    },
    x: {
      grid: { display: false },
      ticks: { color: 'rgba(155, 135, 196, 0.85)' },
    },
  },
}
</script>

<template>
  <div class="h-52">
    <Bar :data="chartData" :options="options" />
  </div>
</template>
