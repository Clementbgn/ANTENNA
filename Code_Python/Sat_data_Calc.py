from skyfield.api import load, EarthSatellite, wgs84
from Antenna_Site import antenna_site
from visibility_periods import is_visible, find_visibility_periods
import os
from datetime import datetime
import json

'''
Satellite Data Calculation for UI 
'''

# Next visibility period calculation

# Directory containing TLE files
directory = "Code_Python/Satellite_data"

# Initialize the list of satellites
TLE_list = []

# Load Skyfield timescale
ts = load.timescale()

# Get the current date and time in UTC
now = datetime.utcnow()


observation_year = now.year
observation_month = now.month
observation_day = now.day
observation_hour = now.hour
observation_minute = now.minute


observation_time = ts.utc(observation_year, observation_month, observation_day, observation_hour, observation_minute)

# Iterate through the files in the directory
for file in os.listdir(directory):
    if file.endswith("_TLE.txt"):  # Check if it is a text file
        
        file_path = os.path.join(directory, file)  # Full path
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
            # Ensure the file contains at least 3 lines
            if len(lines) >= 3:
                sat_name = lines[0].strip()  # Satellite name
                tle_line1 = lines[1].strip()  # First TLE line
                tle_line2 = lines[2].strip()  # Second TLE line

                # Create an EarthSatellite object
                satellite = EarthSatellite(tle_line1, tle_line2, sat_name, ts)

                # Add to the list
                TLE_list.append(satellite)


visible_list = []
az_list = []
el_list = []
last_period_list = []
current_period_list = []
next_period_list = []

# Process each satellite in the TLE list
for sat in TLE_list:
    visible, az, el = is_visible(sat, antenna_site, observation_time)
    visible_list.append(visible)
    az_list.append(az)
    el_list.append(el)
    last_period, current_period, next_period = find_visibility_periods(sat, antenna_site, observation_time)
    last_period_list.append(last_period)
    current_period_list.append(current_period)
    next_period_list.append(next_period)


SATELLITES_INFO = []

# Directory containing JSON files
base_path = "ANTENNA/Code_Python/Satellite_data"

# Get info from all the satellites
for i, sat in enumerate(TLE_list):
    json_filename = os.path.join(base_path, f"{sat.name.replace(' ', '-')}.json")

    try:
        with open(json_filename, "r", encoding="utf-8") as json_file:
            sat_data = json.load(json_file)
            norad = sat_data.get("norad")
            freq = sat_data.get("frequence", "Inconnue")
            ground_station = sat_data.get("ground_station", "Inconnue")
    except FileNotFoundError:
        norad = "Inconnu"
        freq = "Inconnue"
        ground_station = "Inconnue"

    # Extract visibility information
    next_visibility = next_period_list[i]
    next_time_range = f"{next_visibility[0].utc_iso()} - {next_visibility[1].utc_iso()}" if next_visibility else "Aucune - Aucune"
    visible_now = "Oui" if visible_list[i] else "Non"

    # Add the information as a list
    SATELLITES_INFO.append([
        sat.name,        # Satellite name
        norad,           # NORAD number
        freq,            # Reception frequency
        next_time_range, # Next visibility period (start - end)
        visible_now,     # Currently visible (Yes/No)
        ground_station   # Associated ground station
    ])

# Verify the generated data
for sat_info in SATELLITES_INFO:
    print(sat_info)

