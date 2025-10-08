# process.py
from enum import Enum, auto
import math
import time


class State(Enum):
    NEW = "New"
    READY = "Ready"
    RUNNING = "Running"
    WAITING = "Waiting"
    TERMINATED = "Terminated"


class Process:
    def __init__(self, pid: int, name: str, size: int, priority: int = 1, critical=False):
        """
        pid: process id
        name: label for the process
        size: logical memory size in bytes
        priority: integer, higher => runs first
        critical: bool, whether process has critical section
        """
        self.pid = pid
        self.name = name
        self.size = size
        self.pages_needed = None  # computed when page_size known
        self.priority = priority
        self.critical = critical
        self.state = State.NEW
        self.page_table = {}   # vpn -> frame or 'SWAP'
        self.last_run = 0      # for LRU tie-breaker in scheduler (timestamp)
        self.created_at = time.time()

    def set_page_size(self, page_size: int):
        self.pages_needed = (self.size + page_size - 1) // page_size

    def __repr__(self):
        return f"<P{self.pid}:{self.name} pr={self.priority} st={self.state.value} pages={self.pages_needed} crit={self.critical}>"
