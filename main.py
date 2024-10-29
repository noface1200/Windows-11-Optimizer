from tkinter import *
from tkinter import ttk

# Create and configure the Notebook for tabs
def create_notebook(window):
    """Create a Notebook widget to hold multiple tabs."""
    notebook = ttk.Notebook(window)
    tabs = [Frame(notebook) for _ in range(3)]  # Create 3 tabs
    notebook.add(tabs[0], text="Setup & Requirements")  # First tab name
    notebook.add(tabs[1], text="Optimisation")           # Second tab name
    notebook.add(tabs[2], text="Finish")                 # Third tab name
    notebook.pack(expand=True, fill="both")  # Pack the notebook
    return notebook, tabs

# Create the main application window
def create_main_window():
    """Initialize the main window for the application."""
    window = Tk()
    window.title("Windows 11 Optimizer")  # Set the window title
    window.geometry("1000x650")  # Set the window size to 100x650
    window.resizable(False, False)  # Make the window non-resizable
    return window

# Main execution flow
if __name__ == "__main__":
    window = create_main_window()  # Initialize the main window
    notebook, tabs = create_notebook(window)  # Create the notebook and tabs

    # No additional UI components added to the tabs, leaving them empty.

    # Start the main event loop of the application
    window.mainloop()