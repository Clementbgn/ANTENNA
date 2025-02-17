import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from skyfield.api import load, EarthSatellite, wgs84
import tkinter as tk
from tkinter import ttk
from Sat_data_Calc import SATELLITES_INFO, lat_dms,long_dms, az_rise_list,el_rise_list,az_set_list,el_set_list
import Polar_plot 

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
    satellite_tree.delete(*satellite_tree.get_children())  # Clear all current entries

    for sat_info in SATELLITES_INFO:  # Iterate through each satellite
        sat_name = sat_info[0]  # Satellite name (first element)
        norad_id = str(sat_info[1])  # NORAD ID (second element), converted to string for comparison

        # Check if the search term is in the satellite name or the NORAD ID
        if search_term in sat_name.lower() or search_term in norad_id:
            satellite_tree.insert("", "end", values=sat_info)  # Insert the full row



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
        sat_info = satellite_tree.item(selected_item, "values")  # Get selected satellite data

        # Extract known information
        satellite_name = sat_info[0]  # Satellite Name
        norad_id = sat_info[1]  # NORAD ID
        frequency = sat_info[2]  # Frequency
        timeframe = sat_info[3]  
        ground_station_owner = sat_info[5]  # Ground station

        # Extract rise and set times from timeframe
        rise_time, set_time = timeframe.split(" - ") if " - " in timeframe else ("Unknown", "Unknown")

                # Get the list of all items in the treeview (satellite names)
        all_items = satellite_tree.get_children()

        # Find the index of the selected item in the list
        selected_index = all_items.index(selected_item[0])   

        location = f"{lat_dms} - {long_dms}"  # Location of the ground station

        # Rise, Set azimuth & elevation of the selected satellite
        rise_azimuth = az_rise_list[selected_index]
        rise_elevation = el_rise_list[selected_index]
        set_azimuth = az_set_list[selected_index]
        set_elevation = el_set_list[selected_index]

        # Create a new window
        details_window = tk.Toplevel(root)
        details_window.title(f"Satellite Details - {satellite_name}")
        details_window.geometry("400x300")

        # Data dictionary to display
        details = {
            "SATELLITE NAME": satellite_name,
            "NoRad ID": norad_id,
            "Station Name": satellite_name,
            "Location": location,
            "Ground Station Owner": ground_station_owner,
            "Rise Azimuth": rise_azimuth,
            "Set Azimuth": set_azimuth,
            "Rise Elevation": rise_elevation,
            "Set Elevation": set_elevation,
            "Rise Time": rise_time,
            "Set Time": set_time,
            "Frequency": frequency
        }

        # Display each detail in the new window
        for i, (label, value) in enumerate(details.items()):
            tk.Label(details_window, text=f"{label}: {value}", font=("Arial", 12)).pack(pady=5)

# Bind the function to the selection event
satellite_tree.bind("<<TreeviewSelect>>", on_satellite_selected)

root.mainloop()
