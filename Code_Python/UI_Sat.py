import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from skyfield.api import load, EarthSatellite, wgs84
import tkinter as tk
from tkinter import ttk
from Sat_data_Calc import SATELLITES_INFO

# Load available satellites

'''SATELLITES_INFO = {
    "ISS (Zarya)": ["1", "1", "1", "1", "1"],
    "Hubble Space Telescope": ["1", "1", "1", "1", "1"],
    "NOAA 19": ["1", "1", "1", "1", "1"]
}'''







'''
CREATION OF THE UI FOR SATELLITES SELECTION 

'''
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
    for sat, details in SATELLITES_INFO.items():
        if search_term in sat.lower():
            satellite_tree.insert("", "end", values=[sat] + details)

search_var.trace("w", search_satellites)

# Table for satellite information
columns = ("Name", "ID", "Frequency", "Next timeframe", "Visibility", "Ground Station")
satellite_tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    satellite_tree.heading(col, text=col)
    satellite_tree.column(col, width=120)

for sat_info in SATELLITES_INFO:
    satellite_tree.insert("", "end", values=sat_info)

satellite_tree.pack(pady=10, fill=tk.BOTH, expand=True)

def on_satellite_selected(event):
    selected_item = satellite_tree.selection()
    if selected_item:
        sat_name = satellite_tree.item(selected_item, "values")[0]
        print(f"Selected satellite: {sat_name}") 

satellite_tree.bind("<<TreeviewSelect>>", on_satellite_selected)

root.mainloop()
