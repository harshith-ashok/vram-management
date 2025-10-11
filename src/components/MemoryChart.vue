<template>
  <div>
    <canvas ref="mainChart" height="60"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

interface MemoryType {
  name: string
  base: number
}
interface Process {
  name: string
  color: string
  memoryUsage: number
  useGPU: boolean
}

export default defineComponent({
  props: {
    processes: { type: Array as () => Process[], required: true },
    memoryTypes: { type: Array as () => MemoryType[], required: true },
  },
  setup(props) {
    const mainChart = ref<HTMLCanvasElement | null>(null)
    let chartInstance: Chart | null = null

    const createChart = () => {
      const labels = props.processes.map((p) => p.name)

      // System memory caps
      const RAM_CAP = props.memoryTypes.find((m) => m.name === 'RAM')?.base ?? 1024
      const CACHE_CAP = props.memoryTypes.find((m) => m.name === 'Cache')?.base ?? 500
      const ROM_CAP = props.memoryTypes.find((m) => m.name === 'ROM')?.base ?? 32
      const VRAM_CAP = props.memoryTypes.find((m) => m.name === 'VRAM')?.base ?? 8192
      const HDD_CAP = props.memoryTypes.find((m) => m.name === 'HDD')?.base ?? 102400

      const ramData: number[] = []
      const cacheData: number[] = []
      const romData: number[] = []
      const vramData: number[] = []
      const hddData: number[] = []

      // Track total RAM allocated
      let totalRamAllocated = 0

      props.processes.forEach((p) => {
        const requested = p.memoryUsage

        // RAM allocation (system-wide)
        const ramAvailable = Math.max(0, RAM_CAP - totalRamAllocated)
        const ramAllocated = Math.min(requested, ramAvailable)
        totalRamAllocated += ramAllocated

        // Excess goes to HDD
        const hddAllocated = requested - ramAllocated

        // Cache proportional to RAM allocated
        const cacheAllocated = Math.min(ramAllocated * 0.2, CACHE_CAP)

        // ROM fixed
        const romAllocated = ROM_CAP

        // VRAM if GPU checked
        const vramAllocated = p.useGPU ? Math.min(requested * 0.5, VRAM_CAP) : 0

        ramData.push(ramAllocated)
        cacheData.push(cacheAllocated)
        romData.push(romAllocated)
        vramData.push(vramAllocated)
        hddData.push(hddAllocated)
      })

      if (chartInstance) chartInstance.destroy()

      chartInstance = new Chart(mainChart.value!, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            { label: 'RAM', data: ramData, backgroundColor: '#4C7EA8', stack: 'a' },
            { label: 'Cache', data: cacheData, backgroundColor: '#D18E6C', stack: 'a' },
            { label: 'ROM', data: romData, backgroundColor: '#9FBF88', stack: 'a' },
            { label: 'VRAM', data: vramData, backgroundColor: '#7a58a6', stack: 'a' },
            { label: 'HDD', data: hddData, backgroundColor: '#C45A5A', stack: 'a' },
          ],
        },
        options: {
          indexAxis: 'y', // horizontal bars
          responsive: true,
          plugins: { legend: { position: 'bottom' } },
          scales: {
            x: { stacked: true, beginAtZero: true, title: { display: true, text: 'Memory (MB)' } },
            y: { stacked: true },
          },
        },
      })
    }

    onMounted(createChart)
    watch(() => props.processes, createChart, { deep: true })

    return { mainChart }
  },
})
</script>

<!-- <template>
  <div style="max-width: 700px">
    <canvas ref="mainChart" height="180" style="width: 100%"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

interface MemoryType {
  name: string
  base: number
}
interface Process {
  name: string
  color: string
  memoryUsage: number
  useGPU: boolean
}

export default defineComponent({
  props: {
    processes: { type: Array as () => Process[], required: true },
    memoryTypes: { type: Array as () => MemoryType[], required: true },
  },
  setup(props) {
    const mainChart = ref<HTMLCanvasElement | null>(null)
    let chartInstance: Chart | null = null

    const createChart = () => {
      const labels = props.processes.map((p) => p.name)

      // Memory allocation simulation
      const ramMax = props.memoryTypes.find((m) => m.name === 'RAM')?.base ?? 1024
      const cacheMax = props.memoryTypes.find((m) => m.name === 'Cache')?.base ?? 500
      const romMax = props.memoryTypes.find((m) => m.name === 'ROM')?.base ?? 32
      const vramMax = props.memoryTypes.find((m) => m.name === 'VRAM')?.base ?? 8192
      const hddMax = props.memoryTypes.find((m) => m.name === 'HDD')?.base ?? 102400

      const ramData: number[] = []
      const cacheData: number[] = []
      const romData: number[] = []
      const vramData: number[] = []
      const hddData: number[] = []

      props.processes.forEach((p) => {
        // RAM allocation
        const ramUse = Math.min(p.memoryUsage, ramMax)
        const hddUse = Math.max(0, p.memoryUsage - ramMax)

        // Cache proportional to RAM usage
        const cacheUse = Math.min(ramUse * 0.2, cacheMax)

        // ROM fixed per process
        const romUse = Math.min(romMax, romMax)

        // VRAM if GPU checked
        const vramUse = p.useGPU ? Math.min(p.memoryUsage * 0.5, vramMax) : 0

        ramData.push(ramUse)
        cacheData.push(cacheUse)
        romData.push(romUse)
        vramData.push(vramUse)
        hddData.push(hddUse)
      })

      if (chartInstance) chartInstance.destroy()

      chartInstance = new Chart(mainChart.value!, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'RAM',
              data: ramData,
              backgroundColor: '#4A7DA3',
              borderColor: '#35607f',
              borderWidth: 1,
              barThickness: 16,
              stack: 'a',
            },
            {
              label: 'Cache',
              data: cacheData,
              backgroundColor: '#D08A5E',
              borderColor: '#9f623e',
              borderWidth: 1,
              barThickness: 16,
              stack: 'a',
            },
            {
              label: 'ROM',
              data: romData,
              backgroundColor: '#8CBF6E',
              borderColor: '#6b9a53',
              borderWidth: 1,
              barThickness: 16,
              stack: 'a',
            },
            {
              label: 'VRAM',
              data: vramData,
              backgroundColor: '#3EA691',
              borderColor: '#2d8b73',
              borderWidth: 1,
              barThickness: 16,
              stack: 'a',
            },
            {
              label: 'HDD',
              data: hddData,
              backgroundColor: '#C94A4A',
              borderColor: '#8f3333',
              borderWidth: 1,
              barThickness: 16,
              stack: 'a',
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y', // horizontal bars
          plugins: { legend: { position: 'top' } },
          scales: {
            x: { stacked: true, beginAtZero: true, title: { display: true, text: 'Memory (MB)' } },
            y: { stacked: true },
          },
        },
      })
    }

    onMounted(createChart)
    watch(() => props.processes, createChart, { deep: true })

    return { mainChart }
  },
})
</script> -->
