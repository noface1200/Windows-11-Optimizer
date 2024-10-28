# Begin
from tkinter import *
from tkinter import ttk, messagebox
import winreg  # Module for accessing the Windows Registry

# Initialize global variables for checkbox states
checkbox_vars = []  # This will be filled later

# Custom labels for the checkboxes
checkbox_labels = [
    ["Chrome", "Firefox", "Safari", "Edge", "Opera", "Brave", "Vivaldi", "Tor"],  # Browsers
    ["VS Code", "Eclipse", "PyCharm", "Atom", "Sublime Text", "IntelliJ", "NetBeans", "Etc..."],  # Development
    ["Photoshop", "GIMP", "Inkscape", "Canva", "Figma", "Sketch", "CorelDRAW", "Adobe XD"],  # Creativity
    ["Steam", "Epic Games", "Origin", "Battle.net", "Uplay", "GOG", "Xbox App", "Discord"],  # Gaming
    ["Notepad", "TextEdit", "Evernote", "OneNote", "Trello", "Slack", "Zoom", "Skype"]  # Other
]

# Create and configure the Notebook for tabs
def create_notebook(window):
    """Create a Notebook widget to hold multiple tabs."""
    notebook = ttk.Notebook(window)
    tabs = [Frame(notebook) for _ in range(6)]  # Create 6 tabs
    for i in range(6):
        notebook.add(tabs[i], text=f"Tab {i + 1}")  # Add tabs with titles
        if i > 0:
            notebook.tab(tabs[i], state='disabled')  # Disable all but the first tab
    notebook.pack(expand=True, fill="both")  # Pack the notebook
    return notebook, tabs

# Function to enable the next tab in the notebook
def enable_next_tab(current_index):
    """Enable the next tab if it exists and switch to it."""
    if current_index < 5:  # Ensure there is a next tab
        notebook.tab(tabs[current_index + 1], state='normal')  # Enable next tab
        notebook.select(tabs[current_index + 1])  # Switch to next tab

# Prompt user to confirm if a restore point has been created
def check_restore_point(current_index):
    """Prompt user to confirm the creation of a system restore point."""
    response = messagebox.askyesno("Confirm Restore Point", 
                                     "Have you created a system restore point?")
    if response:
        enable_next_tab(current_index)  # Proceed to the next tab
    else:
        messagebox.showinfo("Action Required", "Please create a restore point before continuing.")

# Create checkboxes in a grid layout
def create_checkboxes(frame, labels, vars):
    """Create checkboxes in a grid layout on the specified frame."""
    for row in range(8):
        for col in range(5):
            checkbox = Checkbutton(
                frame,
                text=labels[col][row],
                variable=vars[col][row]
            )
            checkbox.grid(row=row + 1, column=col, padx=15, pady=5)  # Increased padding for better spacing

# Print the states of all checkboxes
def print_checkbox_states():
    """Print the states of all checkboxes in the console."""
    print("Checkbox States:")
    for col in range(5):
        for row in range(8):
            print(f"{checkbox_labels[col][row]}: {checkbox_vars[col][row].get()}")

# Get a list of installed programs from the Windows Registry
def get_installed_programs():
    """Fetch a list of installed programs from the Windows Registry."""
    installed_programs = set()  # Use a set to avoid duplicates
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    # Collect installed programs from specified registry paths
    for path in registry_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    program_name = winreg.QueryValueEx(winreg.OpenKey(reg_key, winreg.EnumKey(reg_key, i)), "DisplayName")[0]
                    installed_programs.add(program_name)
                except (FileNotFoundError, OSError):
                    continue
        except Exception as e:
            print(f"Error accessing {path}: {e}")

    # Access user-specific installed programs
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            try:
                program_name = winreg.QueryValueEx(winreg.OpenKey(reg_key, winreg.EnumKey(reg_key, i)), "DisplayName")[0]
                installed_programs.add(program_name)
            except (FileNotFoundError, OSError):
                continue
    except Exception as e:
        print(f"Error accessing HKEY_CURRENT_USER: {e}")

    return list(installed_programs)  # Return as a list for display

# Function to truncate program names for display
def truncate_program_name(name):
    """Truncate program names longer than 45 characters for display."""
    return name if len(name) <= 45 else name[:42] + "..."

# Create the main application window
def create_main_window():
    """Initialize the main window for the application."""
    global checkbox_vars  # Declare the global variable
    window = Tk()
    window.geometry("600x460")  # Set the window size
    window.resizable(False, False)  # Make the window non-resizable
    
    # Initialize checkbox variables after creating the window
    checkbox_vars = [[BooleanVar() for _ in range(8)] for _ in range(5)]  # 5 columns, 8 rows
    
    return window

# Create the UI for each tab
def create_tab1(tabs):
    """Create components for Tab 1."""
    Label(tabs[0], text="Begin Setup", font=("Helvetica", 18, "bold")).pack(pady=5)
    Label(tabs[0], text="This is some normal text in Tab #1.", font=("Helvetica", 12), width=50).pack(pady=5)
    Label(tabs[0], text="Warning! Make a restore point before continuing!", 
          bg="red", fg="white", font=("Helvetica", 14, "bold"), width=38).pack(pady=5)
    Button(tabs[0], text="Continue to Next Tab", command=lambda: check_restore_point(0)).pack(pady=10)

def create_tab2(tabs):
    """Create components for Tab 2."""
    Label(tabs[1], text="Program Install", font=("Helvetica", 18, "bold")).pack(pady=5)
    checkbox_frame = Frame(tabs[1])
    checkbox_frame.pack(pady=10)
    column_headings = ["Browsers", "Development", "Creativity", "Gaming", "Other"]

    # Create column headings for checkboxes
    for col in range(5):
        Label(checkbox_frame, text=column_headings[col], font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

    # Create checkboxes using the predefined function
    create_checkboxes(checkbox_frame, checkbox_labels, checkbox_vars)

    Button(tabs[1], text="Enable Next Tab", command=lambda: [print_checkbox_states(), enable_next_tab(1)]).pack(pady=10)

def create_tab3(tabs):
    """Create components for Tab 3, displaying installed programs."""
    Label(tabs[2], text="Installed Programs", font=("Helvetica", 18, "bold")).pack(pady=5)
    scrollbar_frame = Frame(tabs[2])
    scrollbar_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(scrollbar_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(scrollbar_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    program_frame = Frame(canvas)
    canvas.create_window((0, 0), window=program_frame, anchor="nw")

    installed_programs = get_installed_programs()  # Fetch installed programs

    # Create checkboxes for installed programs
    for index, program in enumerate(installed_programs):
        var = BooleanVar(value=False)  # Default state is unchecked
        truncated_name = truncate_program_name(program)  # Truncate long names
        checkbox = Checkbutton(program_frame, text=truncated_name, variable=var)
        checkbox.grid(row=index // 2, column=index % 2, sticky='w', padx=10, pady=5)  # Two columns layout

    # Update scrolling region function
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    program_frame.bind("<Configure>", update_scroll_region)

    # Scroll with mouse wheel
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    Button(tabs[2], text="Enable Next Tab", command=lambda: enable_next_tab(2)).pack(pady=10)

def create_tab4(tabs):
    """Create components for Tab 4, customization options."""
    Label(tabs[3], text="Personal Customisations", font=("Helvetica", 18, "bold")).pack(pady=5)
    checkbox_table_frame = Frame(tabs[3])
    checkbox_table_frame.pack(pady=10)

    column_headings_tab4 = ["Modern View", "Taskbar", "Power", "Animations"]
    for col in range(4):
        Label(checkbox_table_frame, text=column_headings_tab4[col], font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

    # Create checkbox variables for Tab 4
    checkbox_vars_tab4 = [[BooleanVar() for _ in range(8)] for _ in range(4)]
    options_tab4 = [
        ["Background", "Profile Icon", "Symbols", "Table Order", "Darkmode", "Feature A6", "Feature A7", "Feature A8"],
        ["Feature B1", "Feature B2", "Feature B3", "Feature B4", "Feature B5", "Feature B6", "Feature B7", "Feature B8"],
        ["Feature C1", "Feature C2", "Feature C3", "Feature C4", "Feature C5", "Feature C6", "Feature C7", "Feature C8"],
        ["Feature D1", "Feature D2", "Feature D3", "Feature D4", "Feature D5", "Feature D6", "Feature D7", "Feature D8"]
    ]

 
    # Create checkboxes for customization options
    for row in range(8):
        for col in range(4): 
            checkbox = Checkbutton(
                checkbox_table_frame,
                text=options_tab4[col][row],
                variable=checkbox_vars_tab4[col][row]
            )
            checkbox.grid(row=row + 1, column=col, padx=15, pady=5)
 
    # Function to print selected options
    def print_selected_options():
        """Print the states of selected customization options."""
        print("Selected Options:")
        for col in range(4):
            for row in range(8):
                option_name = options_tab4[col][row] 
                is_checked = checkbox_vars_tab4[col][row].get()
                print(f"{option_name} = {is_checked} ({'ticked' if is_checked else 'not ticked'})") 

    Button(tabs[3], text="Print Selected Options and Enable Next Tab",
           command=lambda: [print_selected_options(), enable_next_tab(3)]).pack(pady=10)

def create_tab5(tabs):
    """Create components for Tab 5."""
    Label(tabs[4], text="This is Tab #5", width=50, height=25).pack()
    Button(tabs[4], text="Enable Next Tab", command=lambda: enable_next_tab(4)).pack(pady=10)

def create_tab6(tabs):
    """Create components for Tab 6."""
    Label(tabs[5], text="This is Tab #6", width=50, height=25).pack()
    Button(tabs[5], text="Finish", command=lambda: enable_next_tab(5)).pack(pady=10)

# Main execution flow
if __name__ == "__main__":
    window = create_main_window()  # Initialize the main window
    notebook, tabs = create_notebook(window)  # Create the notebook and tabs

    # Create UI components for each tab
    create_tab1(tabs)
    create_tab2(tabs)
    create_tab3(tabs)
    create_tab4(tabs)
    create_tab5(tabs)
    create_tab6(tabs)

    # Start the main event loop of the application
    window.mainloop()

