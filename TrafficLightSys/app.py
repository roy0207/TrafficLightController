import os
import sys

# Get the directory where app.py lives
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build folder where the compiled C++ Python module is located
build_dir = os.path.join(current_dir, "build")

# Add build/ to Python's module search path
if build_dir not in sys.path:
    sys.path.insert(0, build_dir)

# Import your compiled C++ Python module
import TrafficLightSys

# Detect whether we are running in a headless Linux environment
# (for example, GitHub Codespaces with no display available)
is_headless = sys.platform.startswith("linux") and not os.environ.get("DISPLAY")

# Only import tkinter if we actually have a display available
if not is_headless:
    import tkinter as tk


def run_headless_demo():
    """
    Run a simple terminal-based demo when no GUI display is available.

    This is useful in Codespaces or other headless Linux environments.
    It lets the project still run and prove that the backend works,
    even though Tkinter cannot open a real window there.
    """
    print("Headless environment detected.")
    print("Running backend demo instead of Tkinter GUI...")
    print("--------------------------------------------------")

    sim = TrafficLightSys.Simulator(2, 2, 42)

    for _ in range(5):
        sim.step()
        print(f"Time: {sim.getCurrentTime()}")

        for r in range(sim.getRows()):
            for c in range(sim.getCols()):
                cell = sim.getIntersection(r, c)

                state_value = cell.getCurrentStateValue()
                state_text = "NS Green" if state_value == 0 else "EW Green"

                print(f"Intersection [{r}][{c}]")
                print(
                    f"  Queues -> "
                    f"N:{cell.getNorthQueue()} "
                    f"S:{cell.getSouthQueue()} "
                    f"E:{cell.getEastQueue()} "
                    f"W:{cell.getWestQueue()}"
                )
                print(
                    f"  Waits  -> "
                    f"N:{cell.getNorthWaitTime()} "
                    f"S:{cell.getSouthWaitTime()} "
                    f"E:{cell.getEastWaitTime()} "
                    f"W:{cell.getWestWaitTime()}"
                )
                print(
                    f"  Congestion -> "
                    f"NS:{cell.getNSCongestion()} "
                    f"EW:{cell.getEWCongestion()}"
                )
                print(f"  Light: {state_text}")
                print(f"  State Time: {cell.getCurrentStateTime()}")

        print("--------------------------------------------------")


if not is_headless:
    class TrafficApp:
        """
        Main GUI class.

        This version gives you BOTH:
        1. A visual traffic grid drawn on a Canvas
        2. Detailed info boxes for each intersection

        It also makes the whole window scrollable so the bottom row
        of intersection boxes does not get cut off on smaller screens.
        """

        def __init__(self, root):
            self.root = root
            self.root.title("Traffic Light System Viewer")
            self.root.geometry("1200x980")
            self.root.minsize(1000, 820)

            # Create the C++ simulator object
            self.sim = TrafficLightSys.Simulator(2, 2, 42)

            self.rows = self.sim.getRows()
            self.cols = self.sim.getCols()

            # Store info-box labels so we can refresh them
            self.cells = []

            # Track auto-run state
            self.running = False

            # ---------------------------------------------------
            # Make the whole window scrollable
            # ---------------------------------------------------
            self.outer_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
            self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.outer_canvas.yview)
            self.outer_canvas.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side="right", fill="y")
            self.outer_canvas.pack(side="left", fill="both", expand=True)

            # This frame holds ALL visible content
            self.content_frame = tk.Frame(self.outer_canvas, bg="white")
            self.canvas_window = self.outer_canvas.create_window(
                (0, 0),
                window=self.content_frame,
                anchor="nw"
            )

            # Update scroll region whenever content size changes
            self.content_frame.bind("<Configure>", self.on_frame_configure)

            # Make inner frame width follow outer canvas width
            self.outer_canvas.bind("<Configure>", self.on_canvas_configure)

            # Mouse wheel scrolling
            self.outer_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

            # -------------------------------
            # Top title section
            # -------------------------------
            self.title_label = tk.Label(
                self.content_frame,
                text="Traffic Light System Simulation",
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

            # -------------------------------
            # Controls
            # -------------------------------
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

            # -------------------------------
            # Visual traffic grid canvas
            # -------------------------------
            self.canvas_label = tk.Label(
                self.content_frame,
                text="Visual Traffic Grid",
                font=("Arial", 14, "bold"),
                bg="white"
            )
            self.canvas_label.pack(pady=(10, 5))

            self.canvas = tk.Canvas(
                self.content_frame,
                width=920,
                height=360,
                bg="white",
                highlightthickness=1,
                highlightbackground="black"
            )
            self.canvas.pack(pady=10)

            # -------------------------------
            # Detailed info-box section
            # -------------------------------
            self.grid_label = tk.Label(
                self.content_frame,
                text="Intersection Data Boxes",
                font=("Arial", 14, "bold"),
                bg="white"
            )
            self.grid_label.pack(pady=(15, 5))

            self.grid_frame = tk.Frame(self.content_frame, bg="white")
            self.grid_frame.pack(padx=10, pady=10)

            self.create_grid()

            # Initial draw
            self.refresh_display()

        def on_frame_configure(self, event):
            """
            Update the scrollable region whenever the content frame changes size.
            """
            self.outer_canvas.configure(scrollregion=self.outer_canvas.bbox("all"))

        def on_canvas_configure(self, event):
            """
            Make the inner content frame expand to match the visible canvas width.
            """
            self.outer_canvas.itemconfig(self.canvas_window, width=event.width)

        def on_mousewheel(self, event):
            """
            Enable mouse wheel scrolling.
            """
            self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def create_grid(self):
            """
            Create the detailed info-box grid.
            """

            for r in range(self.rows):
                row_widgets = []

                for c in range(self.cols):
                    frame = tk.Frame(
                        self.grid_frame,
                        bd=2,
                        relief="solid",
                        padx=12,
                        pady=12,
                        bg="white"
                    )
                    frame.grid(row=r, column=c, padx=10, pady=10)

                    label = tk.Label(
                        frame,
                        text="Loading...",
                        justify="left",
                        font=("Courier New", 10, "bold"),
                        width=26,
                        height=8,
                        bg="white"
                    )
                    label.pack()

                    row_widgets.append(label)

                self.cells.append(row_widgets)

        def get_light_text(self, state_value):
            """
            Convert C++ integer light state to readable text.
            0 = NS_Green
            1 = EW_Green
            """
            return "NS Green" if state_value == 0 else "EW Green"

        def draw_intersection_visual(self, x, y, cell, label_text):
            """
            Draw one intersection on the canvas as a road crossing.

            Parameters:
                x, y       -> center point of the intersection on the canvas
                cell       -> the C++ Intersection object
                label_text -> like "[0][0]"
            """

            state_value = cell.getCurrentStateValue()

            north = cell.getNorthQueue()
            south = cell.getSouthQueue()
            east = cell.getEastQueue()
            west = cell.getWestQueue()

            # Road colors depend on active direction
            if state_value == 0:
                vertical_color = "green"
                horizontal_color = "red"
            else:
                vertical_color = "red"
                horizontal_color = "green"

            road_width = 18
            road_len = 70

            # Draw north-south road
            self.canvas.create_line(
                x, y - road_len, x, y + road_len,
                fill=vertical_color, width=road_width
            )

            # Draw east-west road
            self.canvas.create_line(
                x - road_len, y, x + road_len, y,
                fill=horizontal_color, width=road_width
            )

            # Draw center intersection square
            self.canvas.create_rectangle(
                x - 12, y - 12, x + 12, y + 12,
                fill="gray25", outline="black"
            )

            # Draw small light indicators
            ns_light_color = "lime" if state_value == 0 else "darkred"
            ew_light_color = "lime" if state_value == 1 else "darkred"

            # NS lights
            self.canvas.create_oval(x - 6, y - 28, x + 6, y - 16, fill=ns_light_color)
            self.canvas.create_oval(x - 6, y + 16, x + 6, y + 28, fill=ns_light_color)

            # EW lights
            self.canvas.create_oval(x - 28, y - 6, x - 16, y + 6, fill=ew_light_color)
            self.canvas.create_oval(x + 16, y - 6, x + 28, y + 6, fill=ew_light_color)

            # Intersection label
            self.canvas.create_text(
                x, y - 95,
                text=f"Intersection {label_text}",
                font=("Arial", 10, "bold")
            )

            # Queue labels around the roads
            self.canvas.create_text(x, y - road_len - 18, text=f"N:{north}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x, y + road_len + 18, text=f"S:{south}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x - road_len - 24, y, text=f"W:{west}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x + road_len + 24, y, text=f"E:{east}", font=("Arial", 10, "bold"))

        def refresh_display(self):
            """
            Refresh both:
            1. visual canvas
            2. detailed info boxes
            """

            # Update time label
            self.time_label.config(text=f"Time: {self.sim.getCurrentTime()}")

            # Clear the canvas before redrawing
            self.canvas.delete("all")

            # Fixed visual positions for 2x2 layout on the canvas
            positions = {
                (0, 0): (220, 110),
                (0, 1): (700, 110),
                (1, 0): (220, 270),
                (1, 1): (700, 270),
            }

            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.sim.getIntersection(r, c)

                    state_value = cell.getCurrentStateValue()
                    light_text = self.get_light_text(state_value)

                    north = cell.getNorthQueue()
                    south = cell.getSouthQueue()
                    east = cell.getEastQueue()
                    west = cell.getWestQueue()

                    north_wait = cell.getNorthWaitTime()
                    south_wait = cell.getSouthWaitTime()
                    east_wait = cell.getEastWaitTime()
                    west_wait = cell.getWestWaitTime()

                    ns_cong = cell.getNSCongestion()
                    ew_cong = cell.getEWCongestion()

                    state_time = cell.getCurrentStateTime()

                    # Color for the info box
                    if state_value == 0:
                        bg_color = "#d4ffd4"   # NS green
                    else:
                        bg_color = "#d4e4ff"   # EW green

                    # Update the detailed info box
                    display_text = (
                        f"Intersection [{r}][{c}]\n"
                        f"Light: {light_text}\n"
                        f"N: {north}   S: {south}\n"
                        f"E: {east}   W: {west}\n"
                        f"N wait: {north_wait}   S wait: {south_wait}\n"
                        f"E wait: {east_wait}   W wait: {west_wait}\n"
                        f"NS Cong: {ns_cong}\n"
                        f"EW Cong: {ew_cong}\n"
                        f"State Time: {state_time}"
                    )

                    self.cells[r][c].config(text=display_text, bg=bg_color)

                    # Draw the visual intersection on the canvas
                    x, y = positions[(r, c)]
                    self.draw_intersection_visual(x, y, cell, f"[{r}][{c}]")

        def step_simulation(self):
            """
            Advance the simulation by one tick, then redraw everything.
            """
            self.sim.step()
            self.refresh_display()

        def auto_run(self):
            """
            Toggle automatic stepping on/off.
            """
            self.running = not self.running

            if self.running:
                self.run_button.config(text="Stop")
                self.run_loop()
            else:
                self.run_button.config(text="Run Automatically")

        def run_loop(self):
            """
            Keep stepping once per second while running is enabled.
            """
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