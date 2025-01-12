# Can print position based on t = t_obs

from skyfield.api import EarthSatellite, Topos, load
from skyfield.api import wgs84
import datetime
import time

ts = load.timescale()

def get_geocentric_position(t_obs,satellite):

    geocentric = satellite.at(t_obs)

    return geocentric

def print_geocentric_postition(t_obs,satellite):

    geocentric = get_geocentric_position(t_obs,satellite)
    print(geocentric)

def get_latitude_longitude(t_obs,satellite):
    geocentric = get_geocentric_position(t_obs,satellite)
    lat_sat, lon_sat = wgs84.latlon_of(geocentric)

    return lat_sat, lon_sat

def print_latitude_longitude_rt(t_obs,satellite):

    lat_sat, lon_sat = get_latitude_longitude(t_obs,satellite)
    print('Latitude:', lat_sat)
    print('Longitude:', lon_sat,"\n")

def get_relative_position_antenna_satellite_AltAz(t_obs,satellite,antenna_site):

    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t_obs)
    alt_sat, az_sat, distance_sat = topocentric.altaz()

    return alt_sat, az_sat, distance_sat

def print_relative_position_antenna_satellite_AltAz(t_obs,satellite,antenna_site):
    
    alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz(t_obs,satellite,antenna_site)
    print("Elevation of the satellite in the sky is: ",alt_sat.degrees)
    print("Azimuth of the satellite in the sky is: ", az_sat.degrees)
    print("Distance of the satellitein the sky is: ", distance_sat.km, "\n")

def get_relative_position_antenna_satellite_RaDec(t_obs,satellite,antenna_site):

    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t_obs)
    ra_sat, dec_sat, distance_sat_radec = topocentric.radec()  # ICRF ("J2000")

    return ra_sat, dec_sat, distance_sat_radec

def print_relative_position_antenna_satellite_RaDec(t_obs,satellite,antenna_site):

    ra_sat, dec_sat, distance_sat_radec = get_relative_position_antenna_satellite_RaDec(t_obs,satellite,antenna_site)
    print("RA of the satellite in the sky:", ra_sat)
    print("DEC of the satellite in the sky:", dec_sat, "\n")

def where_relative_horizon(t_obs,satellite,antenna_site):
    
    alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz(t_obs,satellite,antenna_site)
    if alt_sat.degrees > 0:
        print("The satellite is above the horizon \n")
    else:
        print("The satellite is below the horizon \n")
        




