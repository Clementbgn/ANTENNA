# Can print position based on t = tnow

from skyfield.api import EarthSatellite, Topos, load
from skyfield.api import wgs84
import datetime
import time
import Satellite_list
import Antenna_Site


sat_index = 0 #sat index in Satellite_list.Sats

satellite = Satellite_list.Satellites[sat_index]
antenna_site = Antenna_Site.antenna_site
Satellite_name = Satellite_list.Sats[sat_index]
ts = load.timescale()

def get_geocentric_position():
    t = ts.now()
    geocentric = satellite.at(t)

    return geocentric

def print_geocentric_postition():

    geocentric = get_geocentric_position()
    print(geocentric)

def get_latitude_longitude():
    geocentric = get_geocentric_position()
    lat_sat, lon_sat = wgs84.latlon_of(geocentric)

    return lat_sat, lon_sat

def print_latitude_longitude_rt():

    lat_sat, lon_sat = get_latitude_longitude()
    print('Latitude:', lat_sat)
    print('Longitude:', lon_sat,"\n")

def get_relative_position_antenna_satellite_AltAz():
    t=ts.now()
    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t)
    alt_sat, az_sat, distance_sat = topocentric.altaz()

    return alt_sat, az_sat, distance_sat

def print_relative_position_antenna_satellite_AltAz():
    
    alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz()
    print("Elevation of ",Satellite_name," in the sky is: ",alt_sat.degrees)
    print("Azimuth of ",Satellite_name," in the sky is: ", az_sat.degrees)
    print("Distance of ",Satellite_name," in the sky is: ", distance_sat.km, "\n")

def get_relative_position_antenna_satellite_RaDec():
    t=ts.now()
    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t)
    ra_sat, dec_sat, distance_sat_radec = topocentric.radec()  # ICRF ("J2000")

    return ra_sat, dec_sat, distance_sat_radec

def print_relative_position_antenna_satellite_RaDec():

    ra_sat, dec_sat, distance_sat_radec = get_relative_position_antenna_satellite_RaDec()
    print('RA of ' + Satellite_name + " in the sky:", ra_sat)
    print('DEC of ' + Satellite_name + " in the sky:", dec_sat, "\n")

def where_relative_horizon():
    
    alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz()
    if alt_sat.degrees > 0:
        print( Satellite_name + ' is above the horizon',"\n")
    else:
        print( Satellite_name + ' is below the horizon',"\n")
        




