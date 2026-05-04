import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "build")

if build_dir not in sys.path:
    sys.path.insert(0, build_dir)

import TrafficLightSys

is_headless = sys.platform.startswith("linux") and not os.environ.get("DISPLAY")

if not is_headless:
    import tkinter as tk


def get_light_text(state_value):
    return "NS Green" if state_value == 0 else "EW Green"


def run_headless_demo():
    print("Headless environment detected.")
    print("Running fixed vs adaptive backend demo...")
    print("--------------------------------------------------")

    sim = TrafficLightSys.Simulator(1, 1, 42)

    for _ in range(5):
        sim.step()
        print(f"Time: {sim.getCurrentTime()}")

        fixed = sim.getFixedIntersection(0, 0)
        adaptive = sim.getAdaptiveIntersection(0, 0)

        print("FIXED INTERSECTION")
        print(f"  Light: {get_light_text(fixed.getCurrentStateValue())}")
        print(
            f"  Queues -> "
            f"N:{fixed.getNorthQueue()} "
            f"S:{fixed.getSouthQueue()} "
            f"E:{fixed.getEastQueue()} "
            f"W:{fixed.getWestQueue()}"
        )
        print(f"  Congestion -> NS:{fixed.getNSCongestion()} EW:{fixed.getEWCongestion()}")

        print("ADAPTIVE INTERSECTION")
        print(f"  Light: {get_light_text(adaptive.getCurrentStateValue())}")
        print(
            f"  Queues -> "
            f"N:{adaptive.getNorthQueue()} "
            f"S:{adaptive.getSouthQueue()} "
            f"E:{adaptive.getEastQueue()} "
            f"W:{adaptive.getWestQueue()}"
        )
        print(f"  Congestion -> NS:{adaptive.getNSCongestion()} EW:{adaptive.getEWCongestion()}")

        print("--------------------------------------------------")


if not is_headless:
    class TrafficApp:
        """
        Main GUI class.

        This GUI compares:
        1. One fixed-control intersection
        2. One adaptive-control intersection

        Both receive the same traffic arrivals from the C++ Simulator.
        """

        def __init__(self, root):
            self.root = root
            self.root.title("Traffic Light System Viewer")
            self.root.geometry("1150x850")
            self.root.minsize(950, 760)

            self.sim = TrafficLightSys.Simulator(1, 1, 42)

            self.running = False

            self.outer_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
            self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.outer_canvas.yview)
            self.outer_canvas.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side="right", fill="y")
            self.outer_canvas.pack(side="left", fill="both", expand=True)

            self.content_frame = tk.Frame(self.outer_canvas, bg="white")
            self.canvas_window = self.outer_canvas.create_window(
                (0, 0),
                window=self.content_frame,
                anchor="nw"
            )

            self.content_frame.bind("<Configure>", self.on_frame_configure)
            self.outer_canvas.bind("<Configure>", self.on_canvas_configure)
            self.outer_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

            self.title_label = tk.Label(
                self.content_frame,
                text="Traffic Light System Simulation: Fixed vs Adaptive",
                font=("Arial", 18, "bold"),
                bg="white"
            )
            self.title_label.pack(pady=10)

            self.time_label = tk.Label(
                self.content_frame,
                text="Time: 0",
                font=("Arial", 12),
                bg="white"
            )
            self.time_label.pack(pady=5)

            self.controls_frame = tk.Frame(self.content_frame, bg="white")
            self.controls_frame.pack(pady=10)

            self.step_button = tk.Button(
                self.controls_frame,
                text="Step Simulation",
                command=self.step_simulation,
                width=18
            )
            self.step_button.grid(row=0, column=0, padx=10)

            self.run_button = tk.Button(
                self.controls_frame,
                text="Run Automatically",
                command=self.auto_run,
                width=18
            )
            self.run_button.grid(row=0, column=1, padx=10)

            self.canvas_label = tk.Label(
                self.content_frame,
                text="Visual Comparison",
                font=("Arial", 14, "bold"),
                bg="white"
            )
            self.canvas_label.pack(pady=(10, 5))

            self.canvas = tk.Canvas(
                self.content_frame,
                width=1000,
                height=300,
                bg="white",
                highlightthickness=1,
                highlightbackground="black"
            )
            self.canvas.pack(pady=10)

            self.grid_label = tk.Label(
                self.content_frame,
                text="Detailed Intersection Data",
                font=("Arial", 14, "bold"),
                bg="white"
            )
            self.grid_label.pack(pady=(15, 5))

            self.data_frame = tk.Frame(self.content_frame, bg="white")
            self.data_frame.pack(padx=10, pady=10)

            self.fixed_box = self.make_data_box(self.data_frame, 0, 0, "FIXED CONTROL")
            self.adaptive_box = self.make_data_box(self.data_frame, 0, 1, "ADAPTIVE CONTROL")

            self.refresh_display()

        def on_frame_configure(self, event):
            self.outer_canvas.configure(scrollregion=self.outer_canvas.bbox("all"))

        def on_canvas_configure(self, event):
            self.outer_canvas.itemconfig(self.canvas_window, width=event.width)

        def on_mousewheel(self, event):
            self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def make_data_box(self, parent, row, col, title):
            frame = tk.Frame(
                parent,
                bd=2,
                relief="solid",
                padx=12,
                pady=12,
                bg="white"
            )
            frame.grid(row=row, column=col, padx=20, pady=10)

            heading = tk.Label(
                frame,
                text=title,
                font=("Arial", 12, "bold"),
                bg="white"
            )
            heading.pack(pady=(0, 8))

            label = tk.Label(
                frame,
                text="Loading...",
                justify="left",
                font=("Courier New", 10, "bold"),
                width=30,
                height=9,
                bg="white"
            )
            label.pack()

            return label

        def draw_intersection_visual(self, x, y, cell, label_text):
            state_value = cell.getCurrentStateValue()

            north = cell.getNorthQueue()
            south = cell.getSouthQueue()
            east = cell.getEastQueue()
            west = cell.getWestQueue()

            if state_value == 0:
                vertical_color = "green"
                horizontal_color = "red"
            else:
                vertical_color = "red"
                horizontal_color = "green"

            road_width = 18
            road_len = 70

            self.canvas.create_line(
                x, y - road_len, x, y + road_len,
                fill=vertical_color, width=road_width
            )

            self.canvas.create_line(
                x - road_len, y, x + road_len, y,
                fill=horizontal_color, width=road_width
            )

            self.canvas.create_rectangle(
                x - 12, y - 12, x + 12, y + 12,
                fill="gray25", outline="black"
            )

            ns_light_color = "lime" if state_value == 0 else "darkred"
            ew_light_color = "lime" if state_value == 1 else "darkred"

            self.canvas.create_oval(x - 6, y - 28, x + 6, y - 16, fill=ns_light_color)
            self.canvas.create_oval(x - 6, y + 16, x + 6, y + 28, fill=ns_light_color)

            self.canvas.create_oval(x - 28, y - 6, x - 16, y + 6, fill=ew_light_color)
            self.canvas.create_oval(x + 16, y - 6, x + 28, y + 6, fill=ew_light_color)

            self.canvas.create_text(
                x, y - 95,
                text=label_text,
                font=("Arial", 11, "bold")
            )

            self.canvas.create_text(x, y - road_len - 18, text=f"N:{north}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x, y + road_len + 18, text=f"S:{south}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x - road_len - 24, y, text=f"W:{west}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x + road_len + 24, y, text=f"E:{east}", font=("Arial", 10, "bold"))

        def build_box_text(self, cell):
            return (
                f"Light: {get_light_text(cell.getCurrentStateValue())}\n"
                f"N Queue: {cell.getNorthQueue()}\n"
                f"S Queue: {cell.getSouthQueue()}\n"
                f"E Queue: {cell.getEastQueue()}\n"
                f"W Queue: {cell.getWestQueue()}\n"
                f"N/S Congestion: {cell.getNSCongestion()}\n"
                f"E/W Congestion: {cell.getEWCongestion()}\n"
                f"State Time: {cell.getCurrentStateTime()}"
            )

        def box_color(self, cell, grid_type):
            state = cell.getCurrentStateValue()

            if grid_type == "fixed":
                return "#ffe4cc" if state == 0 else "#ffd0b3"

            return "#d4ffd4" if state == 0 else "#d4e4ff"

        def refresh_display(self):
            self.time_label.config(text=f"Time: {self.sim.getCurrentTime()}")
            self.canvas.delete("all")

            fixed = self.sim.getFixedIntersection(0, 0)
            adaptive = self.sim.getAdaptiveIntersection(0, 0)

            self.canvas.create_text(
                280, 30,
                text="FIXED CONTROL",
                font=("Arial", 15, "bold")
            )

            self.canvas.create_text(
                720, 30,
                text="ADAPTIVE CONTROL",
                font=("Arial", 15, "bold")
            )

            self.draw_intersection_visual(280, 170, fixed, "Fixed Intersection")
            self.draw_intersection_visual(720, 170, adaptive, "Adaptive Intersection")

            self.fixed_box.config(
                text=self.build_box_text(fixed),
                bg=self.box_color(fixed, "fixed")
            )

            self.adaptive_box.config(
                text=self.build_box_text(adaptive),
                bg=self.box_color(adaptive, "adaptive")
            )

        def step_simulation(self):
            self.sim.step()
            self.refresh_display()

        def auto_run(self):
            self.running = not self.running

            if self.running:
                self.run_button.config(text="Stop")
                self.run_loop()
            else:
                self.run_button.config(text="Run Automatically")

        def run_loop(self):
            if self.running:
                self.step_simulation()
                self.root.after(1000, self.run_loop)


if __name__ == "__main__":
    if is_headless:
        run_headless_demo()
    else:
        root = tk.Tk()
        app = TrafficApp(root)
        root.mainloop()