import customtkinter as ctk
import sys
import pkg_resources
import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow modules for image handling
from api import optimisations, personalisations  # Import the lists from api.py

class CustomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Windows-11-Optimizer")
        self.geometry("800x500")

        self.overrideredirect(True)

        self.iconbitmap("images/cookie.ico")

        self.appbar = ctk.CTkFrame(self, height=40, fg_color="#2e3b4e")
        self.appbar.pack(fill="x", side="top", anchor="n")

        # Load the icon image using Pillow
        appbar_icon_image = Image.open("images/cookie.ico")
        appbar_icon_image = appbar_icon_image.resize((20, 20))  # Resize the image to fit the label
        self.appbar_icon = ctk.CTkImage(appbar_icon_image)

        self.appbar_label = ctk.CTkLabel(self.appbar, text="Windows-11-Optimizer", fg_color="#2e3b4e", font=("Helvetica", 16), text_color="white", image=self.appbar_icon, compound="left")
        self.appbar_label.pack(pady=5, padx=20, side="left")

        self.close_button = ctk.CTkButton(self.appbar, text="X", command=self.quit, fg_color="#2e3b4e", text_color="white", width=40, height=40, corner_radius=10)
        self.close_button.pack(pady=5, padx=10, side="right")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=1, fill="both", padx=10, pady=10)

        self.setup_tab = self.tabview.add("Setup")
        self.optimizations_tab = self.tabview.add("Optimisations")
        self.personalisation_tab = self.tabview.add("Personalisation")

        setup_label = ctk.CTkLabel(self.setup_tab, text="Welcome to Setup", font=("Helvetica", 14))
        setup_label.pack(pady=20)

        optimizations_label = ctk.CTkLabel(self.optimizations_tab, text="Optimizer", font=("Helvetica", 14))
        optimizations_label.pack(pady=20)

        personalisation_label = ctk.CTkLabel(self.personalisation_tab, text="Settings", font=("Helvetica", 14))
        personalisation_label.pack(pady=20)

        # For Optimisations tab - dynamically create buttons
        self.optimisation_buttons = []
        for func in optimisations:
            button = ctk.CTkButton(self.optimizations_tab, text=func.__name__.replace("_", " ").title(), command=func)
            button.pack(pady=5)
            self.optimisation_buttons.append(button)

        # For Personalisation tab - dynamically create buttons
        self.personalisation_buttons = []
        for func in personalisations:
            button = ctk.CTkButton(self.personalisation_tab, text=func.__name__.replace("_", " ").title(), command=func)
            button.pack(pady=5)
            self.personalisation_buttons.append(button)

        self._dragging = False
        self._offset_x = 0
        self._offset_y = 0
        self.appbar.bind("<Button-1>", self.start_drag)
        self.appbar.bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        self._dragging = True
        self._offset_x = event.x
        self._offset_y = event.y

    def do_drag(self, event):
        if self._dragging:
            x = self.winfo_x() - self._offset_x + event.x
            y = self.winfo_y() - self._offset_y + event.y
            self.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        self._dragging = False


app = CustomApp()
app.mainloop()
