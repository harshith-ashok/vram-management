# Virtual Memory Management

## Rudimentary OS CLI (Python)

This project is a Python-based simulation of a simple command-line operating system.
It provides a controlled environment to understand the fundamentals of process management, scheduling, and critical section handling through a text-based interface.

---

## Overview

The system functions as a miniature operating system shell that allows users to:

- Create, manage, and terminate simulated processes.
- Define process priorities and critical sections.
- Simulate scheduling algorithms such as Round-Robin or Priority Scheduling.
- Observe synchronization using mutex-based critical section control.

The purpose of this project is educational — to demonstrate core OS concepts in an interactive Python environment.

---

## Features

### Process Management

- Create new processes with specified priority levels.
- Display running, waiting, and terminated processes.
- Manually or automatically terminate processes.

### Scheduling

- Supports both Round-Robin and Priority scheduling.
- Allows configuration of time slices and scheduling intervals.
- Simulates CPU allocation between active processes.

### Critical Sections

- Implements a basic mutual exclusion (mutex) lock system.
- Demonstrates blocking and waiting when a resource is occupied.
- Ensures synchronization between processes.

### Interactive Command-Line Interface

- Simple commands for user interaction:

  - `create <name> <priority>` – Create a process.
  - `list` – View all active processes.
  - `run` – Execute the scheduler.
  - `kill <pid>` – Terminate a process.
  - `lock` / `unlock` – Simulate critical section entry and exit.

---

## Project Structure

```
rudimentary_os_cli/
│
├── os_core/
│   ├── __init__.py
│   ├── process.py           # Defines Process class and states
│   ├── scheduler.py         # Handles scheduling logic
│   ├── critical_section.py  # Manages mutex locks
│
├── cli.py                   # Command-line interface entry point
├── main.py                  # Initializes and runs the OS CLI
└── README.md
```

---

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/rudimentary-os-cli.git
   cd rudimentary-os-cli
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate.bat   # Windows
   ```

3. Run the CLI:

   ```bash
   python main.py
   ```

---

## Example Commands

```
> create process1 3
Process 'process1' created with priority 3.

> create process2 1
Process 'process2' created with priority 1.

> list
PID   Name        Priority   State
1     process1    3          Ready
2     process2    1          Ready

> run
Running scheduler...
Executing process1
Executing process2

> lock
Critical section locked by process1

> unlock
Critical section released
```
