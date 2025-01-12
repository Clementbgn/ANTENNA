from skyfield.api import EarthSatellite, Topos, load
import Satellite_Loader
import Antenna_Site
import realtime_position
import time

ts = load.timescale()

class Reservation:
  def __init__(self, timescale, observation_start, observation_end, observed_object, antenna_location):
    self.ts = timescale
    self.booking_date= ts.now()
    self.observation_start= observation_start #Start Date
    self.observation_end= observation_end #End date
    self.observed_object= observed_object #Norad id
    self.antenna_location= antenna_location

  def isToObserve(self):
    #Compare Now and observation start
    t = self.ts.now()
    if self.observation_start.utc_datetime() <= t.utc_datetime() <= self.observation_end.utc_datetime():
      return True
    else:
      return False
    
  def observe(self):
    if self.isToObserve() == True:
      print('Observable')
    
    else:
      print('Non observable')

    #if is observable: get Azimuth/elev of the sat

  def virtual_observation(self):
    while True:
      realtime_position.print_relative_position_antenna_satellite_AltAz()
      time.sleep(1)
      
