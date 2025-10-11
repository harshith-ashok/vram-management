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

      <!-- Optimize button -->
      <button
        class="btn btn-outline px-6 flex items-center"
        @click="handleOptimize"
        :disabled="optimizing"
      >
        <span v-if="!optimizing">Analyze and optimize with AI</span>
        <span v-else class="flex items-center gap-2">
          <svg
            class="animate-spin h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            ></path>
          </svg>
          Optimizing...
        </span>
      </button>
    </div>

    <div
      v-for="(p, i) in processes"
      :key="p.name"
      class="p-4 border-[0.5px] rounded-md flex gap-3 items-center"
    >
      <!-- Process name with bot badge -->
      <span class="font-medium flex items-center gap-2 justify-center">
        <span
          v-if="p.optimized"
          class="text-white bg-purple-400 p-1 px-3 rounded-full text-sm font-bold flex items-center gap-1"
        >
          AI
        </span>
        {{ p.name }}
      </span>

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
  optimized?: boolean
}

export default defineComponent({
  props: {
    processes: { type: Array as () => Process[], required: true },
  },
  emits: ['updateProcesses', 'addProcess'],
  setup(props, { emit }) {
    const newProcess = ref('')
    const optimizing = ref(false)

    const add = () => {
      if (newProcess.value.trim() !== '') {
        emit('addProcess', newProcess.value.trim())
        newProcess.value = ''
      }
    }

    const handleOptimize = async () => {
      optimizing.value = true
      try {
        const res = await fetch('/api/ollama/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: 'llama3.2',
            prompt: `
You are a system memory optimizer.
Distribute RAM and VRAM usage among these processes efficiently.
EVERY PROCESS SHOULD GET THE MAXIMUM AMOUNT OF RAM AND VRAM WITHOUT COMPROMISING OTHER PROCESSES. IF NOT POSSIBLE PUT IT IN SWAP.
OUTPUT ONLY A SINGLE JSON ARRAY. DO NOT INCLUDE ANY TEXT OR EXPLANATION.
Format:
[
  {"name": "...", "memoryUsage": ..., "useGPU": ...}
]
Processes:
${JSON.stringify(props.processes, null, 2)}
        `,
          }),
        })

        if (!res.ok) throw new Error('Failed to contact LLM')

        const reader = res.body?.getReader()
        if (!reader) throw new Error('No readable stream from Ollama')

        const decoder = new TextDecoder()
        let fullText = ''

        while (true) {
          const { value, done } = await reader.read()
          if (done) break
          fullText += decoder.decode(value, { stream: true })
        }

        // The LLM may return multiple JSON objects line by line; merge the responses
        let accumulated = ''
        fullText.split('\n').forEach((line) => {
          try {
            const obj = JSON.parse(line)
            if (obj.response) accumulated += obj.response
          } catch {
            // skip invalid lines
          }
        })

        // Extract the first valid JSON array
        const match = accumulated.match(/\[.*\]/s)
        if (!match) throw new Error('No JSON array found in LLM output')

        const optimized: Process[] = JSON.parse(match[0]).map((p: Process) => ({
          ...p,
          optimized: true,
        }))

        emit('updateProcesses', optimized)
      } catch (err) {
        console.error('Optimization error:', err)
      } finally {
        optimizing.value = false
      }
    }

    return { newProcess, add, handleOptimize, optimizing }
  },
})
</script>
