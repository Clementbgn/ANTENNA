# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import datetime
import os

def download_TLE(sat_name, sat_norad_id, download_every_N_days):

    #sat_name = "EIRSAT1"  # Name of the satellite ++++ ADD INPUT AUTOMATICALLY LATER
    #sat_norad_id = "58472"  # Norad Id of the satellite ++++ ADD INPUT AUTOMATICALLY LATER
    #download_every_N_days = 2.0  # download again once 2 days old

    name = sat_name + "_TLE.txt"  # custom filename, not 'gp.php'

    path = "Code_Python/Satellite_data/" + name  # Path to load the TLE file

    # Ensure the directory exists
    if not os.path.exists('Code_Python/Satellite_data'):
        os.makedirs('Code_Python/Satellite_data')  # Create the directory if it doesn't exist

    url = ("https://celestrak.org/NORAD/elements/gp.php?CATNR=" + sat_norad_id + "&FORMAT=TLE")  # Generate the url with the Sat query

    if not load.exists(name) or load.days_old(name) >= download_every_N_days:
      load.download(url, filename=path)  # Download the TLE text file after 2 days under Satellite_data


#MAIN

# Create a timescale and ask the current time.
ts = load.timescale()
Satellite_name = "EIRSAT1"
Satellite_Norad_id = "58472"

download_TLE(Satellite_name, Satellite_Norad_id, 2) #Download the TLE of the sat in Satellite_data