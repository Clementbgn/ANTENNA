from skyfield.api import EarthSatellite, Topos, load
from skyfield.api import wgs84
import datetime
import time
import check_visibility


satellite = check_visibility.satellite
antenna_site = check_visibility.antenna_site
Satellite_name = check_visibility.Satellite_name
ts = load.timescale()

def get_geocentric_position_once():
    t = ts.now()
    geocentric = satellite.at(t)

    return geocentric

def get_geocentric_postition_rt():
    while True:
        geocentric = get_geocentric_position_once()
        print(geocentric)
        time.sleep(1)

def get_latitude_longitude_once():
    geocentric = get_geocentric_position_once()
    lat_sat, lon_sat = wgs84.latlon_of(geocentric)

    return lat_sat, lon_sat

def get_latitude_longitude_rt():
    while True:
        lat_sat, lon_sat = get_latitude_longitude_once()
        print('Latitude:', lat_sat)
        print('Longitude:', lon_sat,"\n")
        time.sleep(1)

def get_relative_position_antenna_satellite_AltAz_once():
    t=ts.now()
    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t)
    alt_sat, az_sat, distance_sat = topocentric.altaz()

    return alt_sat, az_sat, distance_sat

def get_relative_position_antenna_satellite_AltAz_rt():
    while True:
        alt_sat, az_sat, distance_sat = get_relative_position_antenna_satellite_AltAz_once()
        print("Elevation of ",Satellite_name," in the sky is: ",alt_sat.degrees)
        print("Azimuth of ",Satellite_name," in the sky is: ", az_sat.degrees)
        print("Distance of ",Satellite_name," in the sky is: ", distance_sat.km, "\n")

        time.sleep(1)

def get_relative_position_antenna_satellite_RaDec_once():
    t=ts.now()
    relative_position_satellite_antenna = satellite - antenna_site
    topocentric = relative_position_satellite_antenna.at(t)
    ra_sat, dec_sat, distance_sat_radec = topocentric.radec()  # ICRF ("J2000")

    return ra_sat, dec_sat, distance_sat_radec

def get_relative_position_antenna_satellite_RaDec_rt():
    while True:
        ra_sat, dec_sat, distance_sat_radec = get_relative_position_antenna_satellite_RaDec_once()
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






