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
    "ISS (Zarya)": ("1 25544U 98067A   23012.21574889  .00016717  00000-0  10270-3 0  9007",
                     "2 25544  51.6434 296.1377 0005793  45.6760 314.4768 15.49912376389561"),
    "Hubble Space Telescope": ("1 20580U 90037B   23012.21574889  .00000273  00000-0  12345-3 0  9003",
                                "2 20580  28.4697 340.5367 0002781  98.5393 261.6123 14.34567890123456"),
    "NOAA 19": ("1 33591U 09005A   23012.21574889  .00000122  00000-0  23456-3 0  9005",
                "2 33591  99.2003 190.5367 0012781  45.6789 314.5123 14.12567890123456")
}


# Function to display available satellites
def search_satellites(*args):
    search_term = search_var.get().lower()
    filtered_satellites = [sat for sat in SATELLITES.keys() if search_term in sat.lower()]
    satellite_list.delete(0, tk.END)
    for sat in filtered_satellites:
        satellite_list.insert(tk.END, sat)

def on_satellite_selected(event):
    selected_sat = satellite_list.get(satellite_list.curselection())
    print(f"Selected satellite: {selected_sat}")  # Placeholder for future functionality

# Create main UI window
root = tk.Tk()
root.title("Satellite Tracker")

search_var = tk.StringVar()
search_var.trace("w", search_satellites)

search_entry = ttk.Entry(root, textvariable=search_var)
search_entry.pack()

satellite_list = tk.Listbox(root)
satellite_list.pack()

for sat in SATELLITES.keys():
    satellite_list.insert(tk.END, sat)

satellite_list.bind("<<ListboxSelect>>", on_satellite_selected)

root.mainloop()
