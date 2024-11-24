# api.py
import os, shutil
# Define the optimisations functions
def clear_cache():
    temp_dir = os.getenv('TEMP')
    try:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except PermissionError:
                print(f"Permission denied: {file_path}")
            except OSError as e:
                print(f"Error removing {file_path}: {e}")
        print("Cache cleared!")
    except Exception as e:
        print(f"Failed to clear cache: {e}")

def power_plan():
    """
    Optimizes power plan for performance.
    """
    print("Power plan optimized!")
    # Add logic to modify power plan settings (e.g., using powercfg command)

# Define the personalisation functions
def change_theme():
    """
    Changes the theme of the system.
    """
    print("Theme changed!")
    # Add logic to change theme (e.g., modify system settings or registry)

def update_display_settings():
    """
    Updates the display settings.
    """
    print("Display settings updated!")
    # Add logic to adjust display settings (e.g., resolution or dual monitor setup)

# Define the lists in api.py
optimisations = [clear_cache, power_plan]  # Functions related to system optimization
personalisations = [change_theme, update_display_settings]  # Functions related to personalisation
