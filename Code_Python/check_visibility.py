# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import datetime
import os
import Satellite_list
import Antenna_Site
import position # Import position to calculate the position at t_obs of a sat
import math

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

def AltAz_at_visibility(visibility,satellite,antenna_site):

    number_of_contacts = str(len(visibility)/3)

    print("\nWe will encounter " + number_of_contacts + " visiblity periods")

    if (number_of_contacts > str(1)):
        j = 1 # Used to determine if it is a rise a culmination or a set
        for i in range(1, int(len(visibility))+1, 1):
            print("Encounter ",math.ceil(i/3))
            t_obs = visibility[i-1]
            alt_sat, az_sat, distance_sat = position.get_relative_position_antenna_satellite_AltAz(t_obs,satellite,antenna_site)

            match j:
                case 1:

                    print("\nRise position: \n" 
                        + "Elevation: ", alt_sat.degrees, " degrees \n"
                        + "Azimuth: ", az_sat.degrees, " degrees \n"
                        + "Distance: ",distance_sat.km ," degrees")
                    print("At ", t_obs.utc_strftime("%Y %b %d %H:%M:%S"),"\n")
                    j=j+1

                

                case 2:

                    print("\nCulmination point position: \n" 
                        + "Elevation: ", alt_sat.degrees, " degrees \n"
                        + "Azimuth: ", az_sat.degrees, " degrees \n"
                        + "Distance: ",distance_sat.km ," degrees")
                    print("At ", t_obs.utc_strftime("%Y %b %d %H:%M:%S"),"\n")
                    j=j+1

                
                case 3:

                    print("\nSet point position: \n" 
                        + "Elevation: ", alt_sat.degrees, " degrees \n"
                        + "Azimuth: ", az_sat.degrees, " degrees \n"
                        + "Distance: ",distance_sat.km ," degrees")
                    print("At ", t_obs.utc_strftime("%Y %b %d %H:%M:%S"),"\n")
                    j=1

                

    

#MAIN

min_elevation = 30
ts = load.timescale()
t0 = ts.now() # First time is now
delta_t = 24 #Delta of the observation in Hour

visibility = check_visibility(Antenna_Site.antenna_site, Satellite_list.Satellites[0], min_elevation, t0, delta_t) #Check visibility of the Satellite from the antenna site

AltAz_at_visibility(visibility,Satellite_list.Satellites[0],Antenna_Site.antenna_site)


