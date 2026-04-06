# Import tkinter for GUI
import tkinter as tk

# Import your compiled C++ Python module
import TrafficLightSys


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

        # Create a button to auto-run the simulation
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
                    padx=10,
                    pady=10
                )
                frame.grid(row=r, column=c, padx=10, pady=10)

                # Create a label inside that frame
                label = tk.Label(
                    frame,
                    text="Loading...",
                    justify="left",
                    font=("Courier New", 10)
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
                light_text = self.get_light_text(cell.getCurrentStateValue())

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

                # Update the label text
                self.cells[r][c].config(text=display_text)

    def step_simulation(self):
        """
        Advance the simulation by one tick,
        then refresh the GUI.
        """

        self.sim.step()
        self.refresh_display()

    def auto_run(self):
        """
        Start automatic stepping of the simulation.

        If already running, do nothing.
        """

        if not self.running:
            self.running = True
            self.run_loop()

    def run_loop(self):
        """
        Repeatedly step the simulation every 1000 ms (1 second)
        while auto-run is enabled.
        """

        if self.running:
            self.step_simulation()

            # Schedule this function to run again after 1 second
            self.root.after(1000, self.run_loop)


# Standard tkinter app startup
if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficApp(root)
    root.mainloop()