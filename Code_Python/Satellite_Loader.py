# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import datetime
import os

ts=load.timescale()

def download_TLE(sat_name, sat_norad_id, download_every_N_days):

    name = sat_name + "_TLE.txt"  # custom filename

    path = "Code_Python/Satellite_data/" + name  # Path to load the TLE file

    # Ensure the directory exists
    if not os.path.exists('Code_Python/Satellite_data'):
        os.makedirs('Code_Python/Satellite_data')  # Create the directory if it doesn't exist

    url = ("https://celestrak.org/NORAD/elements/gp.php?CATNR=" + sat_norad_id + "&FORMAT=TLE")  # Generate the url with the Sat query

    if not does_TLE_exist(sat_name) or load.days_old(name) >= download_every_N_days:
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

def does_TLE_exist(sat_name):
    name = sat_name + "_TLE.txt"  # custom filename, not 'gp.php'
    path = "Code_Python/Satellite_data/" + name  # Path to load the TLE file
    if (os.path.isfile(path) == True):
        return True
    else:
        return False
    
    #AJOUTER POSSIBILITE DE LOAD UN TLE CUSTOM