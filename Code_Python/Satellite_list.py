from skyfield.api import load
import Satellite_Loader

Satellites = [] #creation of the satellite list
Satellites.clear()

ts = load.timescale()

Sats = ["EIRSAT1","CATSAT","CUBEBEL-2"] 
Norad_Ids = ["58472","60246","57175"]

for sat in Sats:
    
    if(Satellite_Loader.does_TLE_exist(sat) == False):
        Satellite_Loader.download_TLE(sat,Norad_Ids[Sats.index(sat)],2)

    satellite = Satellite_Loader.load_TLE(sat, Norad_Ids[Sats.index(sat)]) #Load the TLE data
    Satellites.append(satellite)
    print(Satellites)










