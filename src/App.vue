<template>
  <div class="p-6 space-y-6">
    <h1 class="text-3xl font-bold text-center mb-6">Memory Management Simulator</h1>

    <MemoryChart :processes="processes" :memoryTypes="memoryTypes" />

    <ProcessList
      :processes="processes"
      @updateProcesses="updateProcesses"
      @addProcess="addProcess"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import MemoryChart from './components/MemoryChart.vue'
import ProcessList from './components/ProcessList.vue'

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
  components: { MemoryChart, ProcessList },
  setup() {
    const memoryTypes = ref<MemoryType[]>([
      { name: 'RAM', base: 1024 },
      { name: 'Cache', base: 500 },
      { name: 'ROM', base: 32 },
      { name: 'VRAM', base: 8192 },
      { name: 'HDD', base: 102400 },
    ])

    const processes = ref<Process[]>([
      { name: 'smss.exe', color: 'green', memoryUsage: 130, useGPU: false },
      { name: 'csrss.exe', color: 'red', memoryUsage: 70, useGPU: false },
      { name: 'winlogon.exe', color: 'blue', memoryUsage: 50, useGPU: true },
      { name: 'lsass.exe', color: 'orange', memoryUsage: 100, useGPU: false },
      { name: 'svchost.exe', color: 'teal', memoryUsage: 40, useGPU: false },
      { name: 'explorer.exe', color: 'purple', memoryUsage: 69, useGPU: true },
    ])

    const pastelColors = ['green', 'gray', 'orange', 'black', 'teal']

    const addProcess = (name: string) => {
      const color = pastelColors[processes.value.length % pastelColors.length]
      processes.value.push({ name, color, memoryUsage: 200, useGPU: false })
    }

    const updateProcesses = (updated: Process[]) => {
      processes.value = updated
    }

    return { memoryTypes, processes, addProcess, updateProcesses }
  },
})
</script>
