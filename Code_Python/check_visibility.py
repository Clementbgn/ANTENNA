# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import datetime
import os
import Satellite_Loader
import Antenna_Site
import position # Import position to calculate the 

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

def AltAz_at_visibility(visibility):
    alt_sat, az_sat, distance_sat = position.get_relative_position_antenna_satellite_AltAz()
    

#MAIN

min_elevation = 30
ts = load.timescale()
t0 = ts.now() # First time is now
delta_t = 24 #Delta of the observation in Hour

visibility = check_visibility(Antenna_Site.antenna_site, Satellite_Loader.satellite, min_elevation, t0, delta_t) #Check visibility of the Satellite from the antenna site

print(visibility)

