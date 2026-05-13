import os
import sys

# We need to find folder where app.py file is located.
# compiled C++ module is stored near this file so we can import it
current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "build")

# Add the build folder to Python's search path.
# This lets Python find the compiled TrafficLightSys module.
if build_dir not in sys.path:
    sys.path.insert(0, build_dir)

# Import the C++ backend module created with pybind11.
# This is where our Simulator and Intersection classes come from.
import TrafficLightSys

# Codespaces/Linux usually has no display window available so we adapt for terminal output in that case.
# If there is no DISPLAY variable, we run a terminal demo instead of opening Tkinter.
is_headless = sys.platform.startswith("linux") and not os.environ.get("DISPLAY")

# Only import tkinter when a GUI display is actually available.
if not is_headless:
    import tkinter as tk


def get_light_text(state_value):
    # In the C++ enum, 0 means NS_Green and 1 means EW_Green.
    # This helper converts that number into readable text for the GUI.
    return "NS Green" if state_value == 0 else "EW Green"


def run_headless_demo():
    # This function runs a simple terminal demo of the traffic light system. if py fails to load the GUI.
    print("Headless environment detected.")
    print("Running fixed vs adaptive backend demo...")
    print("--------------------------------------------------")

    # Create one fixed intersection and one adaptive intersection.
    # The seed makes the random traffic pattern repeatable.
    sim = TrafficLightSys.Simulator(1, 1, 42)

    # Run a few steps and print the backend data to the terminal.
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

        This window compares two versions of the traffic light system:
        one fixed-control intersection and one adaptive-control intersection.

        The actual simulation logic is still handled in C++.
        This Python file is mainly responsible for showing the results visually.
        """

        def __init__(self, root):
            # Save the main Tkinter window.
            self.root = root
            self.root.title("Traffic Light System Viewer")
            self.root.geometry("1150x850")
            self.root.minsize(950, 760)

            # Create the C++ simulator.
            # 1 row, 1 column means one fixed intersection and one adaptive intersection.
            # 42 is ourrandom seed so the traffic pattern is repeatable.
            self.sim = TrafficLightSys.Simulator(1, 1, 42)

            # Used to track whether the automatic run mode is on or off.
            self.running = False

            # Main outer canvas makes the window scrollable.
            # This helps if the screen is smaller or the content does not fit.
            self.outer_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
            self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.outer_canvas.yview)
            self.outer_canvas.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side="right", fill="y")
            self.outer_canvas.pack(side="left", fill="both", expand=True)

            # This frame holds everything inside the scrollable canvas.
            self.content_frame = tk.Frame(self.outer_canvas, bg="white")
            self.canvas_window = self.outer_canvas.create_window(
                (0, 0),
                window=self.content_frame,
                anchor="nw"
            )

            # Keep the scroll area updated when the window content changes size.
            self.content_frame.bind("<Configure>", self.on_frame_configure)

            # Make the content frame resize with the outer canvasc.
            self.outer_canvas.bind("<Configure>", self.on_canvas_configure)

            # Allow mouse wheel scrolling if needed .
            self.outer_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

            # Main title for the GUI.
            self.title_label = tk.Label(
                self.content_frame,
                text="Traffic Light System Simulation: Fixed vs Adaptive",
                font=("Arial", 18, "bold"),
                bg="white"
            )
            self.title_label.pack(pady=10)

            # Shows the current simulation time from the C++ backend.
            self.time_label = tk.Label(
                self.content_frame,
                text="Time: 0",
                font=("Arial", 12),
                bg="white"
            )
            self.time_label.pack(pady=5)

            # Frame for the control buttons.
            self.controls_frame = tk.Frame(self.content_frame, bg="white")
            self.controls_frame.pack(pady=10)

            # Button that advances the simulation by one step.
            self.step_button = tk.Button(
                self.controls_frame,
                text="Step Simulation",
                command=self.step_simulation,
                width=18
            )
            self.step_button.grid(row=0, column=0, padx=10)

            # Button that starts or stops the automatic simulation.
            self.run_button = tk.Button(
                self.controls_frame,
                text="Run Automatically",
                command=self.auto_run,
                width=18
            )
            self.run_button.grid(row=0, column=1, padx=10)

            # Label above the visual intersection drawing.
            self.canvas_label = tk.Label(
                self.content_frame,
                text="Visual Comparison",
                font=("Arial", 14, "bold"),
                bg="white"
            )
            self.canvas_label.pack(pady=(10, 5))

            # Canvas where the roads, lights, and queue labels are drawn.
            self.canvas = tk.Canvas(
                self.content_frame,
                width=1000,
                height=300,
                bg="white",
                highlightthickness=1,
                highlightbackground="black"
            )
            self.canvas.pack(pady=10)

            # Label above the data boxes.
            self.grid_label = tk.Label(
                self.content_frame,
                text="Data",
                font=("Arial", 14, "bold"),
                bg="white"
            )
            self.grid_label.pack(pady=(15, 5))

            # Frame that holds the fixed and adaptive data boxes.
            self.data_frame = tk.Frame(self.content_frame, bg="white")
            self.data_frame.pack(padx=10, pady=10)

            # Create one box for fixed control and one box for adaptive control.
            self.fixed_box = self.make_data_box(self.data_frame, 0, 0, "FIXED CONTROL")
            self.adaptive_box = self.make_data_box(self.data_frame, 0, 1, "ADAPTIVE CONTROL")

            # Draw the starting state before any steps are taken.
            self.refresh_display()

        def on_frame_configure(self, event):
            # Update the scrollable area whenever the content frame changes size.
            self.outer_canvas.configure(scrollregion=self.outer_canvas.bbox("all"))

        def on_canvas_configure(self, event):
            # Keep the inner content frame the same width as the visible canvas.
            self.outer_canvas.itemconfig(self.canvas_window, width=event.width)

        def on_mousewheel(self, event):
            # Scroll the main canvas using the mouse wheel.
            self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def make_data_box(self, parent, row, col, title):
            # Creates one bordered data box.
            # These boxes show queue counts, congestion, light state, and timer info.
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
            # Draws one traffic intersection on the canvas.
            # The data comes from the C++ Intersection object passed in as cell.
            state_value = cell.getCurrentStateValue()

            # Get the current queue counts from the C++ backend.
            north = cell.getNorthQueue()
            south = cell.getSouthQueue()
            east = cell.getEastQueue()
            west = cell.getWestQueue()

            # If NS is green, the vertical road is green.
            # If EW is green, the horizontal road is green.
            if state_value == 0:
                vertical_color = "green"
                horizontal_color = "red"
            else:
                vertical_color = "red"
                horizontal_color = "green"

            road_width = 18
            road_len = 70

            # Draw the north/south road.
            self.canvas.create_line(
                x, y - road_len, x, y + road_len,
                fill=vertical_color, width=road_width
            )

            # Draw the east/west road.
            self.canvas.create_line(
                x - road_len, y, x + road_len, y,
                fill=horizontal_color, width=road_width
            )

            # Draw the center of the intersection.
            self.canvas.create_rectangle(
                x - 12, y - 12, x + 12, y + 12,
                fill="gray25", outline="black"
            )

            # Small light indicators around the intersection.
            ns_light_color = "lime" if state_value == 0 else "darkred"
            ew_light_color = "lime" if state_value == 1 else "darkred"

            # North/south lights.
            self.canvas.create_oval(x - 6, y - 28, x + 6, y - 16, fill=ns_light_color)
            self.canvas.create_oval(x - 6, y + 16, x + 6, y + 28, fill=ns_light_color)

            # East/west lights.
            self.canvas.create_oval(x - 28, y - 6, x - 16, y + 6, fill=ew_light_color)
            self.canvas.create_oval(x + 16, y - 6, x + 28, y + 6, fill=ew_light_color)

            # Text label for the intersection.
            self.canvas.create_text(
                x, y - 95,
                text=label_text,
                font=("Arial", 11, "bold")
            )

            # Queue labels around the intersection.
            self.canvas.create_text(x, y - road_len - 18, text=f"N:{north}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x, y + road_len + 18, text=f"S:{south}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x - road_len - 24, y, text=f"W:{west}", font=("Arial", 10, "bold"))
            self.canvas.create_text(x + road_len + 24, y, text=f"E:{east}", font=("Arial", 10, "bold"))

        def build_box_text(self, cell):
            # Builds the text that appears inside the data box.
            # All values are pulled from the C++ Intersection object.
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
            # Gives the data boxes different colors so the two systems are easier to compare.
            # Fixed control uses warmer colors, adaptive control uses green/blue colors.
            state = cell.getCurrentStateValue()

            if grid_type == "fixed":
                return "#ffcccc" if state == 0 else "#ffd0b3"

            return "#d4ffd4" if state == 0 else "#d4e4ff"

        def refresh_display(self):
            # Main GUI refresh function.
            # It reads the latest C++ backend values and redraws both intersections.
            self.time_label.config(text=f"Time: {self.sim.getCurrentTime()}")
            self.canvas.delete("all")

            # Get the fixed and adaptive intersections from the C++ simulator.
            fixed = self.sim.getFixedIntersection(0, 0)
            adaptive = self.sim.getAdaptiveIntersection(0, 0)

            # Labels above each visual intersection.
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

            # Draw both intersections using the latest backend data.
            self.draw_intersection_visual(280, 170, fixed, "Fixed Intersection")
            self.draw_intersection_visual(720, 170, adaptive, "Adaptive Intersection")

            # Update the detailed data boxes under the visual display.
            self.fixed_box.config(
                text=self.build_box_text(fixed),
                bg=self.box_color(fixed, "fixed")
            )

            self.adaptive_box.config(
                text=self.build_box_text(adaptive),
                bg=self.box_color(adaptive, "adaptive")
            )

        def step_simulation(self):
            # Advance the C++ simulation by one step and update the GUI.
            self.sim.step()
            self.refresh_display()

        def auto_run(self):
            # Toggle automatic mode on or off.
            self.running = not self.running

            if self.running:
                self.run_button.config(text="Stop")
                self.run_loop()
            else:
                self.run_button.config(text="Run Automatically")

        def run_loop(self):
            # Keep stepping the simulation every second while automatic mode is on.
            if self.running:
                self.step_simulation()
                self.root.after(1000, self.run_loop)


if __name__ == "__main__":
    # If there is no GUI display, run the terminal version.
    # Otherwise, open the Tkinter window.
    if is_headless:
        run_headless_demo()
    else:
        root = tk.Tk()
        app = TrafficApp(root)
        root.mainloop()