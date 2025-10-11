<template>
  <div class="mt-6 space-y-4">
    <h2 class="text-xl font-semibold mb-2">Processes</h2>
    <div class="flex space-x-2 mb-4">
      <input
        v-model="newProcess"
        placeholder="New process name"
        class="input input-bordered w-[25%]"
      />
      <button class="btn btn-outline px-6" @click="add">Add</button>
    </div>

    <div v-for="(p, i) in processes" :key="p.name" class="p-4 border-[0.5px] rounded-md flex gap-3">
      <span class="font-medium" :style="{ color: p.color }">{{ p.name }}</span>
      <div class="flex items-center space-x-2">
        <input type="checkbox" v-model="p.useGPU" class="checkbox" />
        <label>GPU?</label>
      </div>
      <div class="flex items-center space-x-2 gap-4 mt-2 md:mt-0 w-full md:w-1/2">
        <span class="text-sm w-12">Usage:</span>
        <input
          type="range"
          min="0"
          max="2000"
          v-model.number="p.memoryUsage"
          class="range flex-1"
        />
        <span class="text-sm w-fit">{{ p.memoryUsage }} MB</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

interface Process {
  name: string
  color: string
  memoryUsage: number
  useGPU: boolean
}

export default defineComponent({
  props: {
    processes: { type: Array as () => Process[], required: true },
  },
  emits: ['updateProcesses', 'addProcess'],
  setup(props, { emit }) {
    const newProcess = ref('')

    const add = () => {
      if (newProcess.value.trim() !== '') {
        emit('addProcess', newProcess.value.trim())
        newProcess.value = ''
      }
    }

    // Watchers are not needed because we directly mutate props.processes via v-model
    return { newProcess, add }
  },
})
</script>
