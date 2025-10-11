# Memory Manager Visualization

[![Vue 3](https://img.shields.io/badge/Vue-3.5.22-brightgreen)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-4.1-teal)](https://tailwindcss.com/)
[![DaisyUI](https://img.shields.io/badge/DaisyUI-5.2.3-purple)](https://daisyui.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.5-orange)](https://www.chartjs.org/)
[![Ollama LLM](https://img.shields.io/badge/Ollama-Meta-lightgrey)](https://ollama.com/)

A **Vue 3 + TypeScript** app to simulate system memory management. Visualizes how processes consume RAM, Cache, ROM, VRAM, and HDD, with **interactive sliders** and **AI optimization** using an Ollama LLM.

---

## Features

- Dynamic **stacked horizontal bar chart** for memory usage
- Interactive sliders to control **RAM/VRAM allocation** per process
- **GPU toggle** for VRAM usage
- **AI Optimization**:
  - Optimizes RAM and VRAM distribution
  - Marks optimized processes with a **🤖 badge**

- Light theme with **Tailwind + DaisyUI**

---

## Memory Types & Base Sizes

| Memory Type | Base Size |
| ----------- | --------- |
| RAM         | 1 GB      |
| Cache       | 500 MB    |
| ROM         | 32 MB     |
| VRAM        | 8 GB      |
| HDD         | 100 GB    |

---

## Quick Start

```bash
# Clone repo
git clone <repo_url>
cd memory-manager

# Install dependencies
npm install

# Run dev server
npm run dev
```

Open in browser: `http://localhost:5173`

---

## How to Use

1. **Add a new process** using the input and `Add` button.
2. Adjust **memory usage** with sliders.
3. Toggle **GPU** for VRAM usage.
4. Click **“Optimize with AI”** to redistribute RAM and VRAM efficiently.
5. Chart updates dynamically to reflect changes.

---

## Future Enhancements

- Process priority-based allocation
- Page fault & swap simulation
- CPU usage visualization
- Export snapshots as JSON
