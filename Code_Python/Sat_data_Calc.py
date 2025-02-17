from skyfield.api import load, EarthSatellite, wgs84
from Antenna_Site import antenna_site, lat,long
from visibility_periods import is_visible, find_visibility_periods
import os
from datetime import timedelta
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

def decimal_to_dms(deg, is_latitude=True):
    """Convert decimal coordinates to degrees, minutes, and seconds (DMS) format."""
    direction = "N" if is_latitude and deg >= 0 else "S" if is_latitude else "E" if deg >= 0 else "W"
    deg = abs(deg)
    d = int(deg)
    m = int((deg - d) * 60)
    s = round((deg - d - m / 60) * 3600, 2)
    return f"{d}°{m}'{s}\" {direction}"

# Convert and display
lat_dms = decimal_to_dms(lat, is_latitude=True)
long_dms = decimal_to_dms(long, is_latitude=False)



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
az_rise_list = []
el_rise_list = []
az_set_list = []
el_set_list = []
az_list=[]
el_list=[]
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
    
    # Choisir la période actuelle ou la prochaine si elle n'existe pas
    if current_period:
        period_start = current_period[0].utc_datetime()  # Début de la période actuelle
        period_end = current_period[1].utc_datetime()    # Fin de la période actuelle
    elif next_period:
        period_start = next_period[0].utc_datetime()  # Début de la prochaine période
        period_end = next_period[1].utc_datetime()    # Fin de la prochaine période
    else:
        period_start = period_end = None  # Pas de période valide

    # Si la période est valide, obtenir l'azimuth et l'élévation
    if period_start and period_end:
        # Convertir l'heure de début de la période en objet Time (ts.utc)
        t = ts.utc(period_start.year, period_start.month, period_start.day,
                   period_start.hour, period_start.minute, period_start.second)
        
        # Récupérer l'azimuth et l'élévation pour ce moment
        _, azimuth, elevation = is_visible(sat, antenna_site, t)
        az_rise_list.append(azimuth)
        el_rise_list.append(elevation)
        # Convertir l'heure de début de la période en objet Time (ts.utc)
        t = ts.utc(period_end.year, period_end.month, period_end.day,
                   period_end.hour, period_end.minute, period_end.second)
        
        # Récupérer l'azimuth et l'élévation pour ce moment
        _, azimuth, elevation = is_visible(sat, antenna_site, t)
        az_set_list.append(azimuth)
        el_set_list.append(elevation)
    
print(az_list)
print(el_list)
print(az_rise_list)
print(el_rise_list)
print(az_set_list)
print(el_set_list)

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





