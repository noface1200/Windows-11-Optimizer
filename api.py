# api.py

# Define the optimisations functions
def clear_cache():
    """
    Clears the system cache.
    """
    print("Cache cleared!")
    # Add logic to clear cache (e.g., using subprocess or os commands)

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
