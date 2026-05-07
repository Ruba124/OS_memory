
import tkinter as tk
from tkinter import messagebox
import random

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

class MemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Segmentation Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")

        self.total_size = 0
        self.holes = []
        self.processes = {}

       

        self.method = None
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

    
    def show_memory_input(self):
        self.clear_left()
        
        # 1. Title: "not too up" - give it a top margin of 40-50
        tk.Label(
            self.left, 
            text="Memory Allocation Project", 
            fg="#22c55e", 
            bg="#111827", 
            font=("Arial", 14, "bold")
        ).pack(pady=(50, 10)) # (50 pixels above, 10 pixels below)

        # 2. Input Label: To move it down towards the middle, 
        
        tk.Label(
            self.left, 
            text="Enter Memory Size", 
            fg="white", 
            bg="#111827"
        ).pack(pady=(150, 5)) 

        # 3. Entry Field: Add internal padding (ipady) to make it taller/bigger
        self.mem_entry = tk.Entry(self.left, font=("Arial", 12), width=20)
        self.mem_entry.pack(ipady=8, pady=10)

        # 4. Button
        tk.Button(
            self.left, 
            text="Next", 
            command=self.set_memory, 
            bg="#22c55e", 
            fg="white",
            width=15,
            height=2
        ).pack(pady=20)

    def set_memory(self):
        try:
            self.total_size = int(self.mem_entry.get())
            self.draw_memory()
            self.show_hole_input()
        except:
            messagebox.showerror("Error", "Invalid memory size")

    
    def show_hole_input(self):
        self.clear_left()
        # Push down from top
        tk.Label(self.left, text="Add Holes", fg="white", bg="#111827", font=("Arial", 14, "bold")).pack(pady=(40, 20))

        tk.Label(self.left, text="Start Address", fg="white", bg="#111827").pack()
        self.h_start = tk.Entry(self.left, font=("Arial", 11), width=25)
        self.h_start.pack(pady=10, ipady=5) # Increased pady and ipady

        tk.Label(self.left, text="Hole Size", fg="white", bg="#111827").pack()
        self.h_size = tk.Entry(self.left, font=("Arial", 11), width=25)
        self.h_size.pack(pady=10, ipady=5)

        tk.Button(self.left, text="➕ Add Hole", command=self.add_hole,
                bg="#3b82f6", fg="white", height=2, width=20).pack(pady=15)

        tk.Button(self.left, text="✔ Finish Holes", command=self.finish_holes,
                bg="#22c55e", fg="white", height=2, width=20).pack(pady=5)
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

    def show_process_input(self):
        self.clear_left()

        tk.Label(self.left, text="Process Configuration", fg="white", bg="#111827", font=("Arial", 12, "bold")).pack(pady=(30, 10))

        tk.Label(self.left, text="Process Name", fg="white", bg="#111827").pack()
        self.p_name = tk.Entry(self.left, font=("Arial", 11), width=25)
        self.p_name.pack(pady=10, ipady=5)

        tk.Label(self.left, text="Number of Segments", fg="white", bg="#111827").pack()
        self.p_seg = tk.Entry(self.left, font=("Arial", 11), width=25)
        self.p_seg.pack(pady=10, ipady=5)
        if self.first_allocation:
            tk.Label(self.left, text="Choose Allocation Method",
                    fg="white", bg="#111827", font=("Arial", 12, "bold")).pack(pady=10)

            self.alloc_var = tk.StringVar(value="first")

            self.btn_first = tk.Button(self.left, text="First Fit",
                                    width=20, height=2,
                                    bg="#22c55e", fg="white",
                                    command=lambda: self.select_method("first"))

            self.btn_best = tk.Button(self.left, text="Best Fit",
                                    width=20, height=2,
                                    bg="#374151", fg="white",
                                    command=lambda: self.select_method("best"))

            self.btn_first.pack(pady=5)
            self.btn_best.pack(pady=5)

        tk.Button(self.left, text="Next", command=self.init_segments, bg="#a855f7", fg="white").pack(pady=10)
    def select_method(self, method):
        self.alloc_var.set(method)

        if method == "first":
            self.btn_first.config(bg="#22c55e")   # active
            self.btn_best.config(bg="#374151")    # inactive
        else:
            self.btn_best.config(bg="#22c55e")
            self.btn_first.config(bg="#374151")
    def init_segments(self):
        self.seg_count = int(self.p_seg.get())
        self.current_process = Process(self.p_name.get(), random.choice(self.colors))

        if self.first_allocation:
            self.method = self.alloc_var.get()
            self.first_allocation = False

        self.show_segment_inputs()

    def show_segment_inputs(self):
        self.clear_left()
        self.entries = []

        tk.Label(self.left, text="Enter Segments", fg="white", bg="#111827",
                font=("Arial", 12, "bold")).pack(pady=10)

        for i in range(self.seg_count):
            tk.Label(self.left, text=f"Segment {i+1}", fg="white", bg="#111827").pack()

            tk.Label(self.left, text="Name", fg="white", bg="#111827").pack()
            name = tk.Entry(self.left)
            name.pack(pady=2)

            tk.Label(self.left, text="Size", fg="white", bg="#111827").pack()
            size = tk.Entry(self.left)
            size.pack(pady=2)

            self.entries.append((name, size))

        tk.Button(self.left, text="Allocate", command=self.allocate,
                bg="#22c55e", fg="white", height=2, width=20).pack(pady=10)
    
    
    

    def show_after_alloc(self):
        self.clear_left()

        tk.Button(
            self.left,
            text="➕ Add Process",
            command=self.show_process_input,
            bg="#3b82f6",
            fg="white",
            width=20
        ).pack(pady=10)

        tk.Label(
            self.left,
            text="Click a process to deallocate",
            fg="white",
            bg="#111827",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        self.selected_process = tk.StringVar(value="")
        
        # Dictionary to keep track of buttons by process name
        self.process_buttons = {}

        btn_frame = tk.Frame(self.left, bg="#111827")
        btn_frame.pack(pady=5)

        for name in self.processes.keys():
            btn = tk.Button(
                btn_frame,
                text=name,
                width=25,
                bg="#374151", # Default color
                fg="white",
                command=lambda n=name: self.select_process(n)
            )
            btn.pack(pady=3)
            self.process_buttons[name] = btn # Store reference

        tk.Button(
            self.left,
            text="🗑 Deallocate Selected",
            command=self.deallocate,
            bg="#ef4444",
            fg="white",
            width=20
        ).pack(pady=15)

    def select_process(self, name):
        self.selected_process.set(name)
        
        # Reset all buttons to default color and highlight the selected one
        for p_name, btn in self.process_buttons.items():
            if p_name == name:
                btn.config(bg="#22c55e") # Highlight color (Green)
            else:
                btn.config(bg="#374151") # Default color (Dark Gray)
    def can_allocate(self, process):
    # copy holes (VERY IMPORTANT)
        holes = [Hole(h.start, h.size) for h in self.holes]

        if self.method == "first":
            holes.sort(key=lambda x: x.start)
        else:
            holes.sort(key=lambda x: x.size)

        for seg in process.segments:
            found = False
            for h in holes:
                if h.size >= seg.size:
                    h.start += seg.size
                    h.size -= seg.size
                    found = True
                    break
            if not found:
                return False

        return True
   
    def deallocate(self):
        try:
            name = self.selected_process.get()

            if not name:
                messagebox.showerror("Error", "Please select a process first")
                return

            if name not in self.processes:
                messagebox.showerror("Error", "Process not found")
                return

            process = self.processes.pop(name)

            # return segments to holes
            for seg in process.segments:
                if seg.base is not None:
                    self.holes.append(Hole(seg.base, seg.size))

            self.merge()

            # reset selection
            self.selected_process.set("")

            # refresh UI
            self.draw_memory()
            self.update_tables()
            self.show_after_alloc()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def allocate(self):
        try:
            # ===== 1. CLEAR OLD SEGMENTS =====
            self.current_process.segments = []

            # ===== 2. VALIDATE INPUT =====
            for name, size in self.entries:
                n = name.get().strip()
                s = size.get().strip()

                if not n:
                    messagebox.showerror("Error", "Segment name cannot be empty")
                    return

                if not s.isdigit():
                    messagebox.showerror("Error", f"Invalid size for segment '{n}'")
                    return

                self.current_process.segments.append(
                    Segment(n, int(s), self.current_process.name)
                )

            # ===== 3. CHECK IF PROCESS FITS (ALL-OR-NOTHING) =====
            if not self.can_allocate(self.current_process):
                messagebox.showerror("Fail", "Process does not fit in available holes")
                # Return to the main menu even on failure
                self.show_after_alloc() 
                return

       
            for seg in self.current_process.segments:

                if self.method == "best":
                    self.holes.sort(key=lambda x: x.size)
                else:
                    self.holes.sort(key=lambda x: x.start)

                for h in self.holes:
                    if h.size >= seg.size:
                        seg.base = h.start
                        h.start += seg.size
                        h.size -= seg.size
                        break

            # ===== 6. REMOVE EMPTY HOLES =====
            self.holes = [h for h in self.holes if h.size > 0]

            # ===== 7. SAVE PROCESS =====
            self.processes[self.current_process.name] = self.current_process

            # ===== 8. UPDATE UI =====
            self.draw_memory()
            self.update_tables()
            self.show_after_alloc()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.show_after_alloc() # Ensure we return to the menu on crash

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
            self.canvas.create_text(30, y1, text=str(h.start), fill="white")
            self.canvas.create_text(30, y2, text=str(h.start + h.size), fill="white")

        for p in self.processes.values():
            for s in p.segments:
                y1 = 20 + s.base * scale
                y2 = 20 + (s.base + s.size) * scale
                self.canvas.create_rectangle(60, y1, 260, y2, fill=p.color)
                self.canvas.create_text(30, y1, text=str(s.base), fill="white")
                self.canvas.create_text(30, y2, text=str(s.base + s.size), fill="white")
                self.canvas.create_text(160, (y1+y2)/2, text=f"{p.name}:{s.name}")

    def update_tables(self):
        self.hole_table.delete(1.0, tk.END)
        self.seg_table.delete(1.0, tk.END)

        self.hole_table.insert(tk.END, "HOLES\n")
        for h in self.holes:
            self.hole_table.insert(tk.END, f"Start={h.start} Size={h.size} End={h.start+h.size}\n")

        self.seg_table.insert(tk.END, "SEGMENT TABLE\n")
        for p in self.processes.values():
            self.seg_table.insert(tk.END, f"{p.name}\n")
            for s in p.segments:
                self.seg_table.insert(tk.END, f"{s.name} | Base={s.base} | Size={s.size} | End={s.base+s.size}\n")
            self.seg_table.insert(tk.END, "\n")

    def clear_left(self):
        for w in self.left.winfo_children():
            w.destroy()

root = tk.Tk()
app = MemoryGUI(root)
root.mainloop()
