# Import libraries
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import datetime
import os

def define_observation_site(latitude_site, longitude_site):
    # Define observation site in degrees
    lat = latitude_site
    long = longitude_site
    antenna_site = wgs84.latlon(lat, long)  # position of the antenna on ground CAN BE IMPROVED BY GPS
    return antenna_site

#Observation site
lat = 48.78797485885815
long = 2.0410521528514183

antenna_site = define_observation_site(lat, long) #Define the antenna site