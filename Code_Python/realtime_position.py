from skyfield.api import EarthSatellite, Topos, load
from skyfield.api import wgs84
import datetime
import time
import Satellite_Loader
import Antenna_Site


satellite = Satellite_Loader.satellite
antenna_site = Antenna_Site.antenna_site
Satellite_name = Satellite_Loader.Satellite_name
ts = load.timescale()

def get_geocentric_position():
    t = ts.now()
    geocentric = satellite.at(t)

    return geocentric

def print_geocentric_postition():
    while True:
        geocentric = get_geocentric_position()
        print(geocentric)
        time.sleep(1)

def get_latitude_longitude():
    geocentric = get_geocentric_position()
    lat_sat, lon_sat = wgs84.latlon_of(geocentric)

    return lat_sat, lon_sat

def print_latitude_longitude_rt():
    while True:
        lat_sat, lon_sat = get_latitude_longitude()
        print('Latitude:', lat_sat)
        print('Longitude:', lon_sat,"\n")
        time.sleep(1)

def get_relative_position_antenna_satellite_AltAz():
    t=ts.now()
    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t)
    alt_sat, az_sat, distance_sat = topocentric.altaz()

    return alt_sat, az_sat, distance_sat

def print_relative_position_antenna_satellite_AltAz():
    while True:
        alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz()
        print("Elevation of ",Satellite_name," in the sky is: ",alt_sat.degrees)
        print("Azimuth of ",Satellite_name," in the sky is: ", az_sat.degrees)
        print("Distance of ",Satellite_name," in the sky is: ", distance_sat.km, "\n")

        time.sleep(1)

def get_relative_position_antenna_satellite_RaDec():
    t=ts.now()
    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t)
    ra_sat, dec_sat, distance_sat_radec = topocentric.radec()  # ICRF ("J2000")

    return ra_sat, dec_sat, distance_sat_radec

def print_relative_position_antenna_satellite_RaDec():
    while True:
        ra_sat, dec_sat, distance_sat_radec = get_relative_position_antenna_satellite_RaDec()
        print('RA of ' + Satellite_name + " in the sky:", ra_sat)
        print('DEC of ' + Satellite_name + " in the sky:", dec_sat, "\n")
        time.sleep(1)

def where_relative_horizon():
    while True:
        alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz_once()
        if alt_sat.degrees > 0:
            print( Satellite_name + ' is above the horizon',"\n")
        else:
            print( Satellite_name + ' is below the horizon',"\n")
        time.sleep(1)

#MAIN PART OF THE CODE

print_relative_position_antenna_satellite_AltAz()





