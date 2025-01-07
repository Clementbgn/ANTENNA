# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import os

import datetime
# Create a timescale and ask the current time.
ts = load.timescale()
# Download the TLE file of a specific Sat

Satellite_name = "EIRSAT1"  # Name of the satellite ++++ ADD INPUT AUTOMATICALLY LATER
norad_id = "58472"  # Norad Id of the satellite ++++ ADD INPUT AUTOMATICALLY LATER

max_days = 2.0  # download again once 1 days old
name = Satellite_name + "_TLE.txt"  # custom filename, not 'gp.php'

path = "./Satellite_data/" + name  # Path to load the TLE file

url = (
    "https://celestrak.org/NORAD/elements/gp.php?CATNR=" + norad_id + "&FORMAT=TLE"
)  # Generate the url with the Sat query

os.makedirs("./Satellite_data", exist_ok=True)

# Check if file exists or needs updating
if not os.path.exists(path) or load.days_old(path) >= max_days:
    load.download(url, filename=path)  # Direct download to the correct file

# Load the TLE file
# Load the TLE file
if os.path.exists(path):  # Ensure the file exists
    with open(path, "rb") as f:  # Open in binary mode
        satellites = list(parse_tle_file(f, ts))  # Pass the binary file directly to parse_tle_file
else:
    raise FileNotFoundError(f"TLE file not found: {path}")

print("Loaded", len(satellites), "satellites")

# Load a specific satellite by number
by_number = {sat.model.satnum: sat for sat in satellites}
satellite = by_number[int(norad_id)]
t = ts.now()
#geocentric position
geocentric = satellite.at(t)
print(geocentric.position.km)
#Latitude Longitude of the satellite
lat_sat, lon_sat = wgs84.latlon_of(geocentric)
print('Latitude:', lat_sat)
print('Longitude:', lon_sat)
#Subpoint On map
elevation_m = 300
subpoint = wgs84.latlon(lat_sat.degrees, lon_sat.degrees, elevation_m)
print(subpoint)

# Define observation site : Here Estaca
lat = 48.78797485885815
long = 2.0410521528514183

# Define the min elevation of the sat in the sky to detect a visibility time

min_elevation = 30  # degrees

# Get now as utc time
t = ts.now()

antenna_site = wgs84.latlon(
    lat, long
)  # position of the antenna on ground CAN BE IMPROVED BY GPS

t0 = t  # Start time of the detection [now]
t1 = t + datetime.timedelta(
    hours=24
)  # Addition of a Delta t to analyse for a visibility time here 24 hours

t, events = satellite.find_events(
    antenna_site, t0, t1, altitude_degrees=min_elevation
)  # Find event for rise culminate and set below
event_names = (
    "rise above " + str(min_elevation) + "°",
    "culminate",
    "set below " + str(min_elevation) + "°",
)
for ti, event in zip(t, events):
    name = event_names[event]
    print(ti.utc_strftime("%Y %b %d %H:%M:%S"), name)  # Print events

    
#Find the relative position between the antenna and the satellite
relative_position_satellite_antenna = satellite - antenna_site
topocentric = relative_position_satellite_antenna.at(t)
alt_sat, az_sat, distance_sat = topocentric.altaz()

if alt_sat.degrees > 0:
    print( Satellite_name + ' is above the horizon')
else:
    print( Satellite_name + ' is below the horizon')

print('Altitude of ' + Satellite_name + " in the sky:", alt_sat)
print('Azimuth of ' + Satellite_name + " in the sky:", az_sat)
print('Distance: {:.1f} km'.format(distance_sat.km))

ra_sat, dec_sat, distance_sat_radec = topocentric.radec()  # ICRF ("J2000")

print('RA of ' + Satellite_name + " in the sky:", ra_sat)
print('DEC of ' + Satellite_name + " in the sky:", dec_sat)