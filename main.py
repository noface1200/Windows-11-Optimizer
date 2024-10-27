
from tkinter import *
from tkinter import ttk, messagebox
import winreg  # Import the winreg module for accessing the Windows Registry

# Create the main window
window = Tk()
window.geometry("600x460")  # Set window size to 600x460
window.resizable(False, False)  # Make the window non-resizable

# Global variables for checkboxes
checkbox_vars = [[BooleanVar() for _ in range(8)] for _ in range(5)]  # 5 columns, 8 rows

# Custom labels for checkboxes
checkbox_labels = [
    ["Chrome", "Firefox", "Safari", "Edge", "Opera", "Brave", "Vivaldi", "Tor"],  # Browsers
    ["VS Code", "Eclipse", "PyCharm", "Atom", "Sublime Text", "IntelliJ", "NetBeans", "Xcode"],  # Development
    ["Photoshop", "GIMP", "Inkscape", "Canva", "Figma", "Sketch", "CorelDRAW", "Adobe XD"],  # Creativity
    ["Steam", "Epic Games", "Origin", "Battle.net", "Uplay", "GOG", "Xbox App", "Discord"],  # Gaming
    ["Notepad", "TextEdit", "Evernote", "OneNote", "Trello", "Slack", "Zoom", "Skype"]  # Other
]

# Function to enable the next tab
def enable_next_tab(current_index):
    if current_index < 5:  # Ensure there is a next tab
        notebook.tab(tabs[current_index + 1], state='normal')  # Enable the next tab
        notebook.select(tabs[current_index + 1])  # Switch to the next tab

# Function to check for restore point
def check_restore_point(current_index):
    response = messagebox.askyesno("Confirm Restore Point", 
                                     "Have you created a system restore point?")
    if response:  # If the user clicked 'Yes'
        enable_next_tab(current_index)  # Continue to the next tab
    else:
        messagebox.showinfo("Action Required", "Please create a restore point before continuing.")

# Function to update checkbox state
def update_checkbox(row, col, value):
    checkbox_vars[col][row].set(value)

# Function to print checkbox states
def print_checkbox_states():
    print("Checkbox States:")
    for col in range(5):
        for row in range(8):
            print(f"{checkbox_labels[col][row]}: {checkbox_vars[col][row].get()}")

# Function to get installed programs
def get_installed_programs():
    installed_programs = set()  # Use a set to avoid duplicates
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    for path in registry_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    program_name = winreg.QueryValueEx(winreg.OpenKey(reg_key, winreg.EnumKey(reg_key, i)), "DisplayName")[0]
                    installed_programs.add(program_name)  # Add to set
                except (FileNotFoundError, OSError):
                    continue
        except Exception as e:
            print(f"Error accessing {path}: {e}")

    # Accessing HKEY_CURRENT_USER for installed programs
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            try:
                program_name = winreg.QueryValueEx(winreg.OpenKey(reg_key, winreg.EnumKey(reg_key, i)), "DisplayName")[0]
                installed_programs.add(program_name)  # Add to set
            except (FileNotFoundError, OSError):
                continue
    except Exception as e:
        print(f"Error accessing HKEY_CURRENT_USER: {e}")

    return list(installed_programs)  # Convert back to a list for display

# Store checkbox states for Tab 3
checkbox_vars_tab3 = []

# Function to truncate program names if longer than 45 characters
def truncate_program_name(name):
    return name if len(name) <= 45 else name[:42] + "..."

# Create a Notebook widget
notebook = ttk.Notebook(window)

# Create frames for the tabs
tabs = [Frame(notebook) for _ in range(6)]

# Add tabs to the notebook
notebook.add(tabs[0], text="Tab 1")
notebook.add(tabs[1], text="Tab 2")
notebook.add(tabs[2], text="Tab 3")
notebook.add(tabs[3], text="Tab 4")
notebook.add(tabs[4], text="Tab 5")
notebook.add(tabs[5], text="Tab 6")

# Initially disable all tabs except the first
for i in range(1, 6):
    notebook.tab(tabs[i], state='disabled')

# Pack the notebook
notebook.pack(expand=True, fill="both")

# Tab 1 components
Label(tabs[0], text="Begin Setup", font=("Helvetica", 18, "bold")).pack(pady=5)
Label(tabs[0], text="This is some normal text in Tab #1.", font=("Helvetica", 12), width=50).pack(pady=5)
Label(tabs[0], text="Warning! Make a restore point before continuing!", 
      bg="red", fg="white", font=("Helvetica", 14, "bold"), width=38).pack(pady=5)

# Button for Tab 1
button_tab1 = Button(tabs[0], text="Continue to Next Tab", command=lambda: check_restore_point(0))
button_tab1.pack(pady=10)

# Tab 2 components
Label(tabs[1], text="Program Install", font=("Helvetica", 18, "bold")).pack(pady=5)

# Create an invisible frame for checkboxes
checkbox_frame = Frame(tabs[1])
checkbox_frame.pack(pady=10)

# Create column headings
column_headings = ["Browsers", "Development", "Creativity", "Gaming", "Other"]
for col in range(5):
    Label(checkbox_frame, text=column_headings[col], font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

# Create checkboxes in a 5x8 grid with custom labels
for row in range(8):  # 8 rows
    for col in range(5):  # 5 columns
        checkbox = Checkbutton(
            checkbox_frame,
            text=checkbox_labels[col][row],
            variable=checkbox_vars[col][row],
            command=lambda r=row, c=col: update_checkbox(r, c, checkbox_vars[c][r].get())
        )
        checkbox.grid(row=row + 1, column=col, padx=15, pady=5)  # Increased padx for checkboxes

# Button for Tab 2
button_tab2 = Button(tabs[1], text="Enable Next Tab", command=lambda: [print_checkbox_states(), enable_next_tab(1)])
button_tab2.pack(pady=10)

# Tab 3 components
Label(tabs[2], text="Installed Programs", font=("Helvetica", 18, "bold")).pack(pady=5)

# Create a frame for the scrollbar
scrollbar_frame = Frame(tabs[2])
scrollbar_frame.pack(fill=BOTH, expand=True)

# Create a Canvas widget
canvas = Canvas(scrollbar_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Create a scrollbar
scrollbar = Scrollbar(scrollbar_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
program_frame = Frame(canvas)
canvas.create_window((0, 0), window=program_frame, anchor="nw")

# Fetch installed programs
installed_programs = get_installed_programs()

# Create checkboxes for each installed program in two columns
for index, program in enumerate(installed_programs):
    var = BooleanVar(value=False)  # Default to unchecked
    truncated_name = truncate_program_name(program)  # Truncate long names
    checkbox = Checkbutton(program_frame, text=truncated_name, variable=var)
    checkbox.grid(row=index // 2, column=index % 2, sticky='w', padx=10, pady=5)  # Two columns

    checkbox_vars_tab3.append((program, var))  # Store the program name and its variable

# Update scrolling region
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the frame to the update_scroll_region function
program_frame.bind("<Configure>", update_scroll_region)

# Bind mouse wheel scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Button for Tab 3
def print_installed_programs():
    print("Installed Programs States:")
    for program, var in checkbox_vars_tab3:
        print(f"{program} = {var.get()}")

button_tab3 = Button(tabs[2], text="Enable Next Tab", command=lambda: [print_installed_programs(), enable_next_tab(2)])
button_tab3.pack(pady=10)

# Tab 4 components
Label(tabs[3], text="Personal Customisations", font=("Helvetica", 18, "bold"), width=50).pack(pady=5)

# Create an invisible frame for the checkbox table
checkbox_table_frame = Frame(tabs[3])
checkbox_table_frame.pack(pady=10)

# Create column headings
column_headings_tab4 = ["Modern View", "Taskbar", "Power", "Animations"]
for col in range(4):
    Label(checkbox_table_frame, text=column_headings_tab4[col], font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

# Create checkboxes in a 4x8 grid with unique names for each option
checkbox_vars_tab4 = [[BooleanVar() for _ in range(8)] for _ in range(4)]  # 4 columns, 8 rows

# Define unique names for each option
options_tab4 = [
    ["Background", "Profile Icon", "Symbols", "Table Order", "Darkmode", "Feature A6", "Feature A7", "Feature A8"],
    ["Feature B1", "Feature B2", "Feature B3", "Feature B4", "Feature B5", "Feature B6", "Feature B7", "Feature B8"],
    ["Feature C1", "Feature C2", "Feature C3", "Feature C4", "Feature C5", "Feature C6", "Feature C7", "Feature C8"],
    ["Feature D1", "Feature D2", "Feature D3", "Feature D4", "Feature D5", "Feature D6", "Feature D7", "Feature D8"]
]

for row in range(8):  # 8 rows
    for col in range(4):  # 4 columns
        checkbox = Checkbutton(
            checkbox_table_frame,
            text=options_tab4[col][row],  # Access the specific option name
            variable=checkbox_vars_tab4[col][row]
        )
        checkbox.grid(row=row + 1, column=col, padx=15, pady=5)

# Function to print selected options in the desired format
def print_selected_options():
    print("Selected Options:")
    for col in range(4):
        for row in range(8):
            option_name = options_tab4[col][row]
            is_checked = checkbox_vars_tab4[col][row].get()
            print(f"{option_name} = {is_checked} ({'ticked' if is_checked else 'not ticked'})")

# Button for Tab 4 to print selected options and enable the next tab
button_tab4 = Button(tabs[3], text="Print Selected Options and Enable Next Tab",
                     command=lambda: [print_selected_options(), enable_next_tab(3)])
button_tab4.pack(pady=10)

# Tab 5 components
Label(tabs[4], text="This is Tab #5", width=50, height=25).pack()
button_tab5 = Button(tabs[4], text="Enable Next Tab", command=lambda: enable_next_tab(4))
button_tab5.pack(pady=10)

# Tab 6 components
Label(tabs[5], text="This is Tab #6", width=50, height=25).pack()
button_tab6 = Button(tabs[5], text="Finish", command=lambda: enable_next_tab(5))
button_tab6.pack(pady=10)

# Start the main event loop
window.mainloop()
