# memory.py
import os
import time
import random
from collections import OrderedDict


class MemoryManager:
    def __init__(self, phys_frames=6, page_size=64, swap_path="swap.bin"):
        """
        phys_frames: number of physical frames available
        page_size: bytes per page (simulation)
        swap_path: file path used to simulate swap storage
        """
        self.phys_frames = phys_frames
        self.page_size = page_size
        self.swap_path = swap_path

        # frames: frame_index -> (pid, vpn) or None
        self.frames = [None] * phys_frames

        # reverse mapping: (pid, vpn) -> frame_index (if in memory)
        self.loc = {}

        # swap store: map (pid, vpn) -> swap_offset (we'll just store bytes on disk sequentially)
        self.swap_index = {}

        # LRU book-keeping: OrderedDict key=(pid,vpn) -> last_access_time; most recent at end
        self.lru = OrderedDict()

        # ensure swap file exists (empty)
        with open(self.swap_path, "wb") as f:
            f.truncate(0)

    def allocate_pages_for(self, process):
        """
        Ensure process.page_table entries exist (initially all unmapped -> 'SWAP' or None).
        Does not force load into physical memory for all pages (we lazy load on access).
        """
        process.set_page_size(self.page_size)
        for vpn in range(process.pages_needed):
            # not yet loaded; None means not present
            process.page_table[vpn] = None

    def access(self, process, vpn, write=False):
        """
        Simulate access to virtual page `vpn` of `process`.
        If page present in memory, update LRU and return (hit, frame_index).
        If not present, handle page fault, bring page into a free frame or replace LRU, return (fault, frame_index).
        """
        if vpn < 0 or vpn >= process.pages_needed:
            raise IndexError("Invalid VPN")

        key = (process.pid, vpn)

        # Page present?
        if key in self.loc:
            frame = self.loc[key]
            # update LRU (touch)
            now = time.time()
            if key in self.lru:
                del self.lru[key]
            self.lru[key] = now
            return (True, frame)

        # Page fault — need to load
        frame = self._find_free_frame()
        evicted = None
        if frame is None:
            # evict LRU
            evicted_key, _ = self.lru.popitem(last=False)  # oldest
            evicted = evicted_key  # (pid, vpn)
            frame = self.loc[evicted]
            # write evicted to swap
            self._write_to_swap(evicted)
            # mark evicted process page as swapped-out (we don't have process reference here)
            del self.loc[evicted]

        # load requested page into frame
        self.frames[frame] = key
        self.loc[key] = frame
        now = time.time()
        self.lru[key] = now

        # optional: if we loaded into frame that belonged to evicted, update frames mapping already handled
        return (False, frame, evicted)

    def _find_free_frame(self):
        for i, f in enumerate(self.frames):
            if f is None:
                return i
        return None

    def _write_to_swap(self, key):
        """Simulate writing a page (pid,vpn) to swap: store offset in swap_index"""
        pid, vpn = key
        swap_offset = len(self.swap_index)
        # store a small marker; we don't store real bytes necessary
        self.swap_index[key] = swap_offset
        # append dummy bytes to file to simulate space usage
        with open(self.swap_path, "ab") as f:
            f.write(b'\x00' * self.page_size)
        return swap_offset

    def status(self):
        """Return structured state for UI/debug"""
        frames_info = []
        for i, slot in enumerate(self.frames):
            if slot is None:
                frames_info.append({"frame": i, "pid": None, "vpn": None})
            else:
                pid, vpn = slot
                frames_info.append({"frame": i, "pid": pid, "vpn": vpn})
        return {
            "frames": frames_info,
            "lru_order": list(self.lru.keys()),
            "swap_index": {f"{k[0]}:{k[1]}": v for k, v in self.swap_index.items()}
        }

    def free_process(self, pid):
        """Free any frames belonging to pid and remove swap entries"""
        to_remove = [k for k in self.loc if k[0] == pid]
        for k in to_remove:
            frame = self.loc[k]
            self.frames[frame] = None
            del self.loc[k]
            if k in self.lru:
                del self.lru[k]
        # remove swap entries for pid
        for k in list(self.swap_index.keys()):
            if k[0] == pid:
                del self.swap_index[k]
        # shrink swap file naive approach: we won't compact the file in this simulation

    def debug_print(self):
        print("Frames:")
        for i, f in enumerate(self.frames):
            print(f" [{i}] = {f}")
        print("LRU:", list(self.lru.keys()))
        print("Swap entries:", {
              f"{k[0]}:{k[1]}": v for k, v in self.swap_index.items()})
