import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from skyfield.api import load, EarthSatellite, wgs84
import tkinter as tk
from tkinter import ttk

# Load available satellites
SATELLITES = {
    "ISS (Zarya)": ["25544", "51.6434", "296.1377", "15.4991", "402.68 MHz"],
    "Hubble Space Telescope": ["20580", "28.4697", "340.5367", "14.3456", "436.785 MHz"],
    "NOAA 19": ["33591", "99.2003", "190.5367", "14.1256", "465.987 MHz"]
}

ts = load.timescale()

# Create main UI window
root = tk.Tk()
root.title("Satellite Tracker")
root.geometry("800x600")

# Title Label
title_label = tk.Label(root, text="ESTACA SATELLITE TRACKER", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Search Bar
search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var, width=50)
search_entry.pack(pady=5)

def search_satellites(*args):
    search_term = search_var.get().lower()
    for item in satellite_tree.get_children():
        satellite_tree.delete(item)
    for sat, details in SATELLITES.items():
        if search_term in sat.lower():
            satellite_tree.insert("", "end", values=[sat] + details)

search_var.trace("w", search_satellites)

# Table for satellite information
columns = ("Name", "ID", "Inclination", "RAAN", "Mean Motion", "Frequency")
satellite_tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    satellite_tree.heading(col, text=col)
    satellite_tree.column(col, width=120)

for sat, details in SATELLITES.items():
    satellite_tree.insert("", "end", values=[sat] + details)

satellite_tree.pack(pady=10, fill=tk.BOTH, expand=True)

def on_satellite_selected(event):
    selected_item = satellite_tree.selection()
    if selected_item:
        sat_name = satellite_tree.item(selected_item, "values")[0]
        print(f"Selected satellite: {sat_name}")  # Placeholder for future functionality

satellite_tree.bind("<<TreeviewSelect>>", on_satellite_selected)

root.mainloop()
