# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import datetime
import os

def download_TLE(sat_name, sat_norad_id, download_every_N_days):

    name = sat_name + "_TLE.txt"  # custom filename, not 'gp.php'

    path = "Code_Python/Satellite_data/" + name  # Path to load the TLE file

    # Ensure the directory exists
    if not os.path.exists('Code_Python/Satellite_data'):
        os.makedirs('Code_Python/Satellite_data')  # Create the directory if it doesn't exist

    url = ("https://celestrak.org/NORAD/elements/gp.php?CATNR=" + sat_norad_id + "&FORMAT=TLE")  # Generate the url with the Sat query

    if not load.exists(name) or load.days_old(name) >= download_every_N_days:
      load.download(url, filename=path)  # Download the TLE text file after 2 days under Satellite_data

def load_TLE(sat_name,sat_norad_id):
   # Load the TLE file
    name = sat_name + "_TLE.txt"  # custom filename, not 'gp.php'
    path = "Code_Python/Satellite_data/" + name  # Path to load the TLE file
    with load.open(path) as f:
        satellites = list(parse_tle_file(f, ts))
        print("Loaded", len(satellites), "satellites")
    # Load a specific satellite by number
    by_number = {sat.model.satnum: sat for sat in satellites}
    satellite = by_number[int(sat_norad_id)]

    return satellite

def define_observation_site(latitude_site, longitude_site):
    # Define observation site in degrees
    lat = latitude_site
    long = longitude_site
    antenna_site = wgs84.latlon(lat, long)  # position of the antenna on ground CAN BE IMPROVED BY GPS
    return antenna_site

def check_visibility(antenna_site, satellite, minimum_elevation, t0, delta_t):
    
    visibility = [] #Create a list of Visibility times in UTC

# Define the min elevation of the sat in the sky to detect a visibility time

    min_elevation = minimum_elevation  # degrees

    t0 = t0  # Start time of the detection [now]
    t1 = t0 + datetime.timedelta(hours=delta_t)  # Addition of a Delta t to analyse for a visibility time here 24 hours

    t, events = satellite.find_events(antenna_site, t0, t1, altitude_degrees=min_elevation)  # Find event for rise culminate and set below
    event_names = (
    "rise above " + str(min_elevation) + "°",
    "culminate",
    "set below " + str(min_elevation) + "°",
    )
    for ti, event in zip(t, events):
        name = event_names[event]
        print(ti.utc_strftime("%Y %b %d %H:%M:%S"), name)  # Print events
        visibility.append(ti) 
    return visibility
#MAIN

#Parameters
Satellite_name = "EIRSAT1"
Satellite_Norad_id = "58472"
#Observation site
lat = 48.78797485885815
long = 2.0410521528514183
#Observation Parameters
min_elevation = 30
ts = load.timescale()
t0 = ts.now() # First time is now
delta_t = 24 #Delta of the observation in Hour

# Create a timescale

download_TLE(Satellite_name, Satellite_Norad_id, 2) #Download the TLE of the sat in Satellite_data
satellite = load_TLE(Satellite_name, Satellite_Norad_id) #Load the TLE data
antenna_site = define_observation_site(lat, long) #Define the antenna site
visibility = check_visibility(antenna_site, satellite, min_elevation, t0, delta_t) #Check visibility of the Satellite from the antenna site

print(visibility)
