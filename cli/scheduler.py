# scheduler.py
import heapq
import time
from collections import deque
from process import State


class Scheduler:
    def __init__(self):
        # ready queues per priority (higher integer => higher priority)
        # We'll use a dict priority -> deque of process objects
        self.ready = {}
        self.blocked = set()  # pids that are waiting (e.g., waiting for IO or in critical)
        self.running = None
        self.time_slice = 1.0  # seconds per step (simulated)
        self.last_tick = time.time()

    def add(self, process):
        # don't add terminated processes
        if process.state == State.TERMINATED:
            return
        pr = process.priority
        if pr not in self.ready:
            self.ready[pr] = deque()
        self.ready[pr].append(process)
        process.state = State.READY
        process.last_run = time.time()

    def pick_next(self):
        if self.running and self.running.critical:
            # If the currently running process is in critical section, it continues until it leaves
            return self.running
        # choose highest priority non-empty queue
        if not self.ready:
            return None
        for pr in sorted(self.ready.keys(), reverse=True):
            q = self.ready[pr]
            while q:
                proc = q.popleft()
                if proc.state != State.TERMINATED:
                    proc.state = State.RUNNING
                    proc.last_run = time.time()
                    self.running = proc
                    return proc
        return None

    def preempt_if_needed(self, incoming):
        """
        If incoming has higher priority than running and running isn't in critical, preempt.
        """
        if self.running is None:
            return False
        if self.running.critical:
            return False
        if incoming.priority > self.running.priority:
            # preempt
            self.running.state = State.READY
            self.add(self.running)
            self.running = None
            return True
        return False

    def block(self, process):
        process.state = State.WAITING
        self.blocked.add(process.pid)

    def unblock(self, process):
        if process.pid in self.blocked:
            self.blocked.remove(process.pid)
            self.add(process)

    def status(self):
        return {
            "running": (self.running.pid if self.running else None),
            "ready": {pr: [p.pid for p in q] for pr, q in self.ready.items()},
            "blocked": list(self.blocked)
        }
