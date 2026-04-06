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
        This class manages the whole GUI application.

        It is responsible for:
        - creating the simulator
        - building the tkinter layout
        - updating the simulation
        - refreshing what the user sees
        """

        def __init__(self, root):
            """
            Constructor for the GUI app.

            Parameters:
                root -> the main tkinter window
            """

            # Save the tkinter root window
            self.root = root

            # Set the title shown in the window bar
            self.root.title("Traffic Light System Viewer")

            # Create the C++ simulator object
            # Grid size = 2x2
            # Seed = 42 for repeatable results
            self.sim = TrafficLightSys.Simulator(2, 2, 42)

            # Ask the simulator how large the grid is
            self.rows = self.sim.getRows()
            self.cols = self.sim.getCols()

            # This will store tkinter label widgets for each intersection
            # So we can update them later
            self.cells = []

            # Create a title label at the top of the GUI
            self.title_label = tk.Label(
                root,
                text="Traffic Light System Simulation",
                font=("Arial", 16, "bold")
            )
            self.title_label.pack(pady=10)

            # Create a label to show the current simulation time
            self.time_label = tk.Label(
                root,
                text="Time: 0",
                font=("Arial", 12)
            )
            self.time_label.pack(pady=5)

            # Create a frame to hold the 2x2 grid
            self.grid_frame = tk.Frame(root)
            self.grid_frame.pack(padx=10, pady=10)

            # Build the visible grid of intersection panels
            self.create_grid()

            # Create a button to advance the simulation one step manually
            self.step_button = tk.Button(
                root,
                text="Step Simulation",
                command=self.step_simulation
            )
            self.step_button.pack(pady=5)

            # Create a button to auto-run / stop the simulation
            self.run_button = tk.Button(
                root,
                text="Run Automatically",
                command=self.auto_run
            )
            self.run_button.pack(pady=5)

            # Track whether auto-run is enabled
            self.running = False

            # Draw the initial state before any steps happen
            self.refresh_display()

        def create_grid(self):
            """
            Create the 2x2 grid of panels.

            Each panel is a frame containing one label.
            The label text will later be updated with intersection state.
            """

            for r in range(self.rows):
                row_widgets = []

                for c in range(self.cols):
                    # Create a bordered frame for one intersection
                    frame = tk.Frame(
                        self.grid_frame,
                        bd=2,
                        relief="solid",
                        padx=15,
                        pady=15
                    )
                    frame.grid(row=r, column=c, padx=10, pady=10)

                    # Create a label inside that frame
                    label = tk.Label(
                        frame,
                        text="Loading...",
                        justify="left",
                        font=("Courier New", 11, "bold"),
                        width=26,
                        height=10
                    )
                    label.pack()

                    # Save the label so we can update it later
                    row_widgets.append(label)

                self.cells.append(row_widgets)

        def get_light_text(self, state_value):
            """
            Convert the C++ light state integer into readable text.

            In your C++ enum:
                0 = NS_Green
                1 = EW_Green
            """

            if state_value == 0:
                return "NS Green"
            else:
                return "EW Green"

        def refresh_display(self):
            """
            Read the latest simulation state from C++
            and update every label in the GUI.
            """

            # Update the time label at the top
            self.time_label.config(text=f"Time: {self.sim.getCurrentTime()}")

            # Loop through every intersection in the grid
            for r in range(self.rows):
                for c in range(self.cols):
                    # Get the C++ Intersection object for this cell
                    cell = self.sim.getIntersection(r, c)

                    # Read all the values we want to display
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

                    # Color the cell differently depending on light state
                    if state_value == 0:
                        bg_color = "#d4ffd4"   # light green for NS green
                    else:
                        bg_color = "#d4e4ff"   # light blue for EW green

                    # Build the text shown inside the label
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

                    # Update the label text and background color
                    self.cells[r][c].config(text=display_text, bg=bg_color)

        def step_simulation(self):
            """
            Advance the simulation by one tick,
            then refresh the GUI.
            """

            self.sim.step()
            self.refresh_display()

        def auto_run(self):
            """
            Toggle automatic stepping of the simulation.
            """

            self.running = not self.running

            if self.running:
                self.run_button.config(text="Stop")
                self.run_loop()
            else:
                self.run_button.config(text="Run Automatically")

        def run_loop(self):
            """
            Repeatedly step the simulation every 1000 ms (1 second)
            while auto-run is enabled.
            """

            if self.running:
                self.step_simulation()

                # Schedule this function to run again after 1 second
                self.root.after(1000, self.run_loop)


if __name__ == "__main__":
    if is_headless:
        run_headless_demo()
    else:
        root = tk.Tk()
        app = TrafficApp(root)
        root.mainloop()