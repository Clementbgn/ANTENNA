# Can print position based on t = t_obs

from skyfield.api import EarthSatellite, Topos, load
from skyfield.api import wgs84
import datetime
import time
import Satellite_Loader
import Antenna_Site
import keyboard

satellite = Satellite_Loader.satellite
antenna_site = Antenna_Site.antenna_site
Satellite_name = Satellite_Loader.Satellite_name
ts = load.timescale()

def get_geocentric_position(t_obs):

    geocentric = satellite.at(t_obs)

    return geocentric

def print_geocentric_postition(t_obs):

    geocentric = get_geocentric_position(t_obs)
    print(geocentric)

def get_latitude_longitude(t_obs):
    geocentric = get_geocentric_position(t_obs)
    lat_sat, lon_sat = wgs84.latlon_of(geocentric)

    return lat_sat, lon_sat

def print_latitude_longitude_rt(t_obs):

    lat_sat, lon_sat = get_latitude_longitude(t_obs)
    print('Latitude:', lat_sat)
    print('Longitude:', lon_sat,"\n")

def get_relative_position_antenna_satellite_AltAz(t_obs):

    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t_obs)
    alt_sat, az_sat, distance_sat = topocentric.altaz()

    return alt_sat, az_sat, distance_sat

def print_relative_position_antenna_satellite_AltAz(t_obs):
    
    alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz(t_obs)
    print("Elevation of ",Satellite_name," in the sky is: ",alt_sat.degrees)
    print("Azimuth of ",Satellite_name," in the sky is: ", az_sat.degrees)
    print("Distance of ",Satellite_name," in the sky is: ", distance_sat.km, "\n")

def get_relative_position_antenna_satellite_RaDec(t_obs):

    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t_obs)
    ra_sat, dec_sat, distance_sat_radec = topocentric.radec()  # ICRF ("J2000")

    return ra_sat, dec_sat, distance_sat_radec

def print_relative_position_antenna_satellite_RaDec(t_obs):

    ra_sat, dec_sat, distance_sat_radec = get_relative_position_antenna_satellite_RaDec(t_obs)
    print('RA of ' + Satellite_name + " in the sky:", ra_sat)
    print('DEC of ' + Satellite_name + " in the sky:", dec_sat, "\n")

def where_relative_horizon(t_obs):
    
    alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz(t_obs)
    if alt_sat.degrees > 0:
        print( Satellite_name + ' is above the horizon',"\n")
    else:
        print( Satellite_name + ' is below the horizon',"\n")
        




