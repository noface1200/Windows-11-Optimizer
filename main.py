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

    # Disable tab switching by overriding the default behavior
    notebook.bind("<<NotebookTabChanged>>", lambda e: lock_tabs(notebook))

    # Add navigation buttons
    add_navigation_buttons(tabs, notebook)

    # Initially lock all tabs except the first
    lock_tabs(notebook)

    return notebook, tabs

def lock_tabs(notebook):
    """Lock all tabs except the currently selected one."""
    current_index = notebook.index(notebook.select())
    for index in range(len(notebook.tabs())):
        if index == current_index:
            notebook.tab(index, state="normal")  # Unlock current tab
        else:
            notebook.tab(index, state="disabled")  # Lock other tabs

def add_navigation_buttons(tabs, notebook):
    """Add forward and backward buttons to each tab."""
    for index, tab in enumerate(tabs):
        # Create a frame to center the buttons
        button_frame = Frame(tab)
        button_frame.pack(side=BOTTOM, pady=10)

        # Create navigation buttons
        back_button = Button(button_frame, text="Back", command=lambda i=index: navigate_tabs(i, -1, notebook))
        forward_button = Button(button_frame, text="Forward", command=lambda i=index: navigate_tabs(i, 1, notebook))

        # Place buttons in the frame
        back_button.pack(side=LEFT, padx=5)
        forward_button.pack(side=RIGHT, padx=5)

def navigate_tabs(current_index, direction, notebook):
    """Navigate to the next or previous tab."""
    new_index = current_index + direction
    if 0 <= new_index < len(notebook.tabs()):
        # Unlock the new tab before moving
        notebook.tab(new_index, state="normal")  # Unlock the next or previous tab
        notebook.select(new_index)                # Move to the new tab
        lock_tabs(notebook)                       # Lock all other tabs
    else:
        print("Error: Cannot navigate further in that direction.")

# Create the main application window
def create_main_window():
    """Initialize the main window for the application."""
    window = Tk()
    window.title("Windows 11 Optimizer")  # Set the window title
    window.geometry("1000x650")  # Set the window size to 1000x650
    window.resizable(False, False)  # Make the window non-resizable
    return window

# Main execution flow
if __name__ == "__main__":
    window = create_main_window()  # Initialize the main window
    notebook, tabs = create_notebook(window)  # Create the notebook and tabs

    # Start the main event loop of the application
    window.mainloop()