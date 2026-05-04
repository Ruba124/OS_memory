import tkinter as tk
from tkinter import messagebox
import random

# ================= DATA =================
class Hole:
    def __init__(self, start, size):
        self.start = start
        self.size = size

class Segment:
    def __init__(self, name, size, parent):
        self.name = name
        self.size = size
        self.parent = parent
        self.base = None

class Process:
    def __init__(self, name, color):
        self.name = name
        self.segments = []
        self.color = color

# ================= GUI =================
class MemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Segmentation Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")

        self.total_size = 0
        self.holes = []
        self.processes = {}

        self.method = None  # first or best
        self.first_allocation = True

        self.colors = ["#38bdf8","#a78bfa","#34d399","#fbbf24","#fb7185"]

        self.setup_ui()

    def setup_ui(self):
        self.left = tk.Frame(self.root, bg="#111827", width=320)
        self.left.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(self.root, width=320, height=650, bg="#020617", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, padx=10)

        self.hole_table = tk.Text(self.root, width=30, bg="#020617", fg="white")
        self.hole_table.pack(side=tk.RIGHT)

        self.seg_table = tk.Text(self.root, width=40, bg="#020617", fg="white")
        self.seg_table.pack(side=tk.RIGHT)

        self.show_memory_input()

    # ================= STEP 1 =================
    def show_memory_input(self):
        self.clear_left()
        tk.Label(self.left, text="Enter Memory Size", fg="white", bg="#111827").pack(pady=10)
        self.mem_entry = tk.Entry(self.left)
        self.mem_entry.pack()
        tk.Button(self.left, text="Next", command=self.set_memory, bg="#22c55e", fg="white").pack(pady=10)

    def set_memory(self):
        try:
            self.total_size = int(self.mem_entry.get())
            self.draw_memory()
            self.show_hole_input()
        except:
            messagebox.showerror("Error", "Invalid memory size")

    # ================= STEP 2 =================
    def show_hole_input(self):
        self.clear_left()
        tk.Label(self.left, text="Add Holes", fg="white", bg="#111827").pack(pady=5)

        self.h_start = tk.Entry(self.left)
        self.h_start.pack()
        self.h_size = tk.Entry(self.left)
        self.h_size.pack()

        tk.Button(self.left, text="Add Hole", command=self.add_hole, bg="#3b82f6", fg="white").pack(pady=5)
        tk.Button(self.left, text="Finish Holes", command=self.finish_holes, bg="#22c55e", fg="white").pack(pady=5)

    def add_hole(self):
        try:
            start = int(self.h_start.get())
            size = int(self.h_size.get())

            if start + size > self.total_size:
                messagebox.showerror("Error", "Hole exceeds memory")
                return

            for h in self.holes:
                if not (start+size <= h.start or start >= h.start+h.size):
                    messagebox.showerror("Error", "Overlap")
                    return

            self.holes.append(Hole(start, size))
            self.draw_memory()
            self.update_tables()

        except:
            messagebox.showerror("Error", "Invalid hole")

    def finish_holes(self):
        self.show_process_input()

    # ================= STEP 3 =================
    def show_process_input(self):
        self.clear_left()

        tk.Label(self.left, text="Process Name", fg="white", bg="#111827").pack()
        self.p_name = tk.Entry(self.left)
        self.p_name.pack()

        tk.Label(self.left, text="Number of Segments", fg="white", bg="#111827").pack()
        self.p_seg = tk.Entry(self.left)
        self.p_seg.pack()

        if self.first_allocation:
            tk.Label(self.left, text="Allocation Type", fg="white", bg="#111827").pack()
            self.alloc_var = tk.StringVar(value="first")
            tk.Radiobutton(self.left, text="First Fit", variable=self.alloc_var, value="first", bg="#111827", fg="white").pack()
            tk.Radiobutton(self.left, text="Best Fit", variable=self.alloc_var, value="best", bg="#111827", fg="white").pack()

        tk.Button(self.left, text="Next", command=self.init_segments, bg="#a855f7", fg="white").pack(pady=10)

    def init_segments(self):
        self.seg_inputs = []
        self.seg_count = int(self.p_seg.get())
        self.current_process = Process(self.p_name.get(), random.choice(self.colors))

        if self.first_allocation:
            self.method = self.alloc_var.get()
            self.first_allocation = False

        self.show_segment_inputs()

    def show_segment_inputs(self):
        self.clear_left()
        self.entries = []

        for i in range(self.seg_count):
            tk.Label(self.left, text=f"Segment {i+1}", fg="white", bg="#111827").pack()
            name = tk.Entry(self.left)
            name.pack()
            size = tk.Entry(self.left)
            size.pack()
            self.entries.append((name, size))

        tk.Button(self.left, text="Allocate", command=self.allocate, bg="#22c55e", fg="white").pack(pady=10)

    # ================= ALLOC =================
    def allocate(self):
        try:
            for name, size in self.entries:
                self.current_process.segments.append(
                    Segment(name.get(), int(size.get()), self.current_process.name)
                )

            holes = sorted(self.holes, key=lambda x: x.start)
            if self.method == "best":
                holes = sorted(self.holes, key=lambda x: x.size)

            temp = []
            for seg in self.current_process.segments:
                found = False
                for h in holes:
                    if h.size >= seg.size:
                        temp.append((seg, h))
                        found = True
                        break
                if not found:
                    messagebox.showerror("Fail", "Process does not fit")
                    return

            for seg, h in temp:
                seg.base = h.start
                h.start += seg.size
                h.size -= seg.size

            self.holes = [h for h in holes if h.size > 0]
            self.processes[self.current_process.name] = self.current_process

            self.draw_memory()
            self.update_tables()
            self.show_after_alloc()

        except:
            messagebox.showerror("Error", "Invalid segment input")

    # ================= AFTER =================
    def show_after_alloc(self):
        self.clear_left()

        tk.Button(self.left, text="Add Process", command=self.show_process_input, bg="#3b82f6", fg="white").pack(pady=10)

        self.proc_var = tk.StringVar()
        if self.processes:
            self.proc_var.set(list(self.processes.keys())[0])

        tk.OptionMenu(self.left, self.proc_var, *self.processes.keys()).pack()
        tk.Button(self.left, text="Deallocate", command=self.deallocate, bg="#ef4444", fg="white").pack(pady=10)

    # ================= DEALLOC =================
    def deallocate(self):
        name = self.proc_var.get()
        if name in self.processes:
            p = self.processes.pop(name)
            for s in p.segments:
                self.holes.append(Hole(s.base, s.size))

            self.merge()
            self.draw_memory()
            self.update_tables()
            self.show_after_alloc()

    def merge(self):
        self.holes.sort(key=lambda x: x.start)
        merged = []
        for h in self.holes:
            if not merged:
                merged.append(h)
            else:
                last = merged[-1]
                if last.start + last.size == h.start:
                    last.size += h.size
                else:
                    merged.append(h)
        self.holes = merged

    # ================= DRAW =================
    def draw_memory(self):
        self.canvas.delete("all")
        if self.total_size == 0:
            return

        scale = 600 / self.total_size

        self.canvas.create_rectangle(60, 20, 260, 620, outline="#38bdf8")

        for h in self.holes:
            y1 = 20 + h.start * scale
            y2 = 20 + (h.start + h.size) * scale
            self.canvas.create_rectangle(60, y1, 260, y2, fill="#64748b")
            self.canvas.create_text(160, (y1+y2)/2, text=f"HOLE\n{h.start}-{h.start+h.size}", fill="white")

        for p in self.processes.values():
            for s in p.segments:
                y1 = 20 + s.base * scale
                y2 = 20 + (s.base + s.size) * scale
                self.canvas.create_rectangle(60, y1, 260, y2, fill=p.color)
                self.canvas.create_text(160, (y1+y2)/2, text=f"{p.name}:{s.name}")

    # ================= TABLES =================
    def update_tables(self):
        self.hole_table.delete(1.0, tk.END)
        self.seg_table.delete(1.0, tk.END)

        self.hole_table.insert(tk.END, "HOLES\n")
        for h in self.holes:
            self.hole_table.insert(tk.END, f"Start={h.start} Size={h.size}\n")

        self.seg_table.insert(tk.END, "SEGMENT TABLE\n")
        for p in self.processes.values():
            self.seg_table.insert(tk.END, f"{p.name}\n")
            for s in p.segments:
                self.seg_table.insert(tk.END, f"{s.name} | Base={s.base} | Size={s.size}\n")
            self.seg_table.insert(tk.END, "\n")

    def clear_left(self):
        for w in self.left.winfo_children():
            w.destroy()

# ================= RUN =================
root = tk.Tk()
app = MemoryGUI(root)
root.mainloop()

