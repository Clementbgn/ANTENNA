from skyfield.api import EarthSatellite, Topos, load
import Satellite_Loader
import Antenna_Site


class Reservation:
  def __init__(self, observation_start, observation_end, observed_object, antenna_location):
    ts = load.timescale()
    self.booking_date= ts.now()
    self.observation_start= observation_start #Start Date
    self.observation_end= observation_end #End date
    self.observed_object= observed_object #Norad id
    self.antenna_location= antenna_location

  def isToObserve(self):
    #Compare Now and observation start
    t = self.ts.now()
    if self.observation_start <= t and t <= self.observation_end:
      return True
    else:
      return False

  def observe(self):
    if self.isToObserve() == True:
      print('Observable')
    
    else:
      print('Non observable')

    #if is observable: get Azimuth/elev of the sat
