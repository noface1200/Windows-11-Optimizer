from tkinter import *
from tkinter import ttk
import pygame  # Import pygame for sound playback
import os      # Import os for clearing the console

# Function to clear the console
def clear_console():
    """Clear the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to play the startup sound
def play_startup_sound():
    """Play the startup sound when the application starts."""
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load("sounds/startup_sound.mp3")  # Load the sound file
    pygame.mixer.music.play()  # Play the sound
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set an event when the sound ends

# Function to play a click sound
def play_click_sound():
    """Play the click sound for button actions."""
    pygame.mixer.music.load("sounds/click_movement_button.mp3")  # Load the click sound
    pygame.mixer.music.play()  # Play the click sound

# Create and configure the Notebook for tabs
def create_notebook(window):
    """Create a Notebook widget to hold multiple tabs."""
    notebook = ttk.Notebook(window)
    tabs = [Frame(notebook) for _ in range(3)]  # Create 3 tabs
    notebook.add(tabs[0], text="Setup & Requirements")  # First tab name
    notebook.add(tabs[1], text="Optimisation")           # Second tab name
    notebook.add(tabs[2], text="Finish")                 # Third tab name
    notebook.pack(expand=True, fill="both")  # Pack the notebook

    # Add navigation buttons (outside the tabs)
    global back_button, forward_button
    back_button, forward_button = add_navigation_buttons(window)

    # Initially lock all tabs except the first
    lock_tabs(notebook)
    update_button_visibility(notebook)

    # Bind tab change event
    notebook.bind("<<NotebookTabChanged>>", lambda e: update_button_visibility(notebook))

    return notebook, tabs

def lock_tabs(notebook):
    """Lock all tabs except the currently selected one."""
    current_index = notebook.index(notebook.select())
    for index in range(len(notebook.tabs())):
        if index == current_index:
            notebook.tab(index, state="normal")  # Unlock current tab
        else:
            notebook.tab(index, state="disabled")  # Lock other tabs

def add_navigation_buttons(window):
    """Add forward and backward buttons to the main window."""
    button_frame = Frame(window)  # Create a frame for buttons in the main window
    button_frame.pack(side=BOTTOM, pady=10)

    # Create navigation buttons
    back_button = Button(button_frame, text="Back", command=lambda: navigate_tabs(-1))
    forward_button = Button(button_frame, text="Forward", command=lambda: navigate_tabs(1))

    # Place buttons in the frame
    back_button.pack(side=LEFT, padx=5)
    forward_button.pack(side=RIGHT, padx=5)

    return back_button, forward_button

def navigate_tabs(direction):
    """Navigate to the next or previous tab and play sound."""
    play_click_sound()  # Play the click sound
    current_index = notebook.index(notebook.select())
    new_index = current_index + direction
    if 0 <= new_index < len(notebook.tabs()):
        # Unlock the new tab before moving
        notebook.tab(new_index, state="normal")  # Unlock the next or previous tab
        notebook.select(new_index)                # Move to the new tab
        lock_tabs(notebook)                       # Lock all other tabs
        update_button_visibility(notebook)        # Update button visibility
    else:
        print("Error: Cannot navigate further in that direction.")

def update_button_visibility(notebook):
    """Update the visibility of navigation buttons based on the current tab."""
    current_index = notebook.index(notebook.select())
    
    if current_index == 0:  # First tab
        back_button.pack_forget()  # Hide back button
    else:
        back_button.pack(side=LEFT, padx=5)  # Show back button

    if current_index == len(notebook.tabs()) - 1:  # Last tab
        forward_button.pack_forget()  # Hide forward button
    else:
        forward_button.pack(side=RIGHT, padx=5)  # Show forward button

# Create the main application window
def create_main_window():
    """Initialize the main window for the application."""
    window = Tk()
    window.title("Windows 11 Optimizer")  # Set the window title
    window.geometry("1000x650")  # Set the window size to 1000x650
    window.resizable(False, False)  # Make the window non-resizable
    window.iconbitmap("images/cookie.ico")  # Set the window icon
    return window

# Main execution flow
if __name__ == "__main__":
    window = create_main_window()  # Initialize the main window
    play_startup_sound()  # Play the startup sound

    # Clear the console after the sound starts playing
    clear_console()

    notebook, tabs = create_notebook(window)  # Create the notebook and tabs

    # Start the main event loop of the application
    window.mainloop()