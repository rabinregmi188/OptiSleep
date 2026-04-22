<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  distribution: number[]
  averageQuality: number
}>()

const chartData = computed(() => ({
  labels: ['Terrible', 'Poor', 'Okay', 'Good', 'Excellent'],
  datasets: [
    {
      data: props.distribution,
      backgroundColor: ['#f87171', '#fb923c', '#fbbf24', '#34d399', '#a78bfa'],
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '72%',
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#17122a',
      borderColor: 'rgba(167,139,250,0.22)',
      borderWidth: 1,
      callbacks: {
        label: (ctx: any) => `${ctx.label}: ${ctx.raw} nights`,
      },
    },
  },
}
</script>

<template>
  <div class="relative h-44">
    <Doughnut :data="chartData" :options="options" />
    <div class="pointer-events-none absolute inset-0 flex items-center justify-center">
      <div class="text-center">
        <p class="opti-title text-3xl font-extrabold leading-none">{{ averageQuality }}</p>
        <p class="text-[10px] uppercase tracking-[0.08em]" style="color: var(--text-soft);">
          avg quality
        </p>
      </div>
    </div>
  </div>
</template>
