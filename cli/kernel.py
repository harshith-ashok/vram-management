# kernel.py
import time
import threading
from process import Process, State
from memory import MemoryManager
from scheduler import Scheduler


class RudimentaryKernel:
    def __init__(self, phys_frames=6, page_size=64):
        self.mm = MemoryManager(phys_frames=phys_frames, page_size=page_size)
        self.scheduler = Scheduler()
        self.next_pid = 1
        self.processes = {}  # pid -> Process
        self.lock = threading.Lock()
        self.running = False
        self.sim_thread = None

    def create_process(self, name, size, priority=1, critical=False):
        pid = self.next_pid
        self.next_pid += 1
        proc = Process(pid, name, size, priority=priority, critical=critical)
        proc.set_page_size(self.mm.page_size)
        self.mm.allocate_pages_for(proc)
        proc.state = State.READY
        self.processes[pid] = proc
        self.scheduler.add(proc)
        print(f"[Kernel] Created {proc}")
        return pid

    def kill_process(self, pid):
        if pid not in self.processes:
            print("[Kernel] No such PID")
            return
        proc = self.processes[pid]
        proc.state = State.TERMINATED
        self.mm.free_process(pid)
        print(f"[Kernel] Killed PID {pid}")

    def step(self):
        """Perform a single scheduling & memory access step"""
        proc = self.scheduler.pick_next()
        if not proc:
            print("[Kernel] No process ready to run")
            return
        print(f"[Kernel] Running {proc}")
        # Simulate that running touches all its pages one by one (for demo); each touch may cause page faults
        for vpn in range(proc.pages_needed):
            res = self.mm.access(proc, vpn)
            if res[0] is True:
                # hit
                print(
                    f"  [Memory] HIT P{proc.pid} vpn={vpn} -> frame={res[1]}")
            else:
                # fault: res = (False, frame, evicted) or (False, frame)
                evicted = res[2] if len(res) > 2 else None
                print(
                    f"  [Memory] FAULT P{proc.pid} vpn={vpn} -> loaded frame={res[1]} evicted={evicted}")
                # In a real OS we'd update proc.page_table; here loc mapping suffices
            time.sleep(0.05)  # small delay to simulate cost

        # Finish time slice
        proc.state = State.READY
        self.scheduler.add(proc)
        print(f"[Kernel] Time slice over for P{proc.pid}")

    def run(self, interval=1.0):
        self.running = True

        def loop():
            while self.running:
                with self.lock:
                    self.step()
                time.sleep(interval)
        self.sim_thread = threading.Thread(target=loop, daemon=True)
        self.sim_thread.start()
        print("[Kernel] Started simulation thread")

    def stop(self):
        self.running = False
        if self.sim_thread:
            self.sim_thread.join(timeout=1.0)
        print("[Kernel] Stopped simulation")

    def inspect(self):
        print("=== KERNEL INSPECT ===")
        for pid, p in self.processes.items():
            print(p)
        print(self.mm.status())
        print(self.scheduler.status())


def repl():
    kern = RudimentaryKernel(phys_frames=6, page_size=64)
    print("Rudimentary OS Kernel (type 'help')")
    while True:
        cmd = input("kernel> ").strip().split()
        if not cmd:
            continue
        c = cmd[0].lower()
        if c == "help":
            print(
                "commands: create <name> <size> [priority] [critical:0/1], kill <pid>, step, run, stop, inspect, view, exit")
        elif c == "create":
            if len(cmd) < 3:
                print("usage: create <name> <size> [priority] [critical]")
                continue
            name = cmd[1]
            size = int(cmd[2])
            pr = int(cmd[3]) if len(cmd) > 3 else 1
            crit = bool(int(cmd[4])) if len(cmd) > 4 else False
            kern.create_process(name, size, priority=pr, critical=crit)
        elif c == "kill":
            pid = int(cmd[1])
            kern.kill_process(pid)
        elif c == "step":
            kern.step()
        elif c == "run":
            kern.run(interval=1.0)
        elif c == "stop":
            kern.stop()
        elif c == "inspect" or c == "view":
            kern.inspect()
        elif c == "exit" or c == "quit":
            kern.stop()
            break
        else:
            print("unknown:", c)


if __name__ == "__main__":
    repl()
