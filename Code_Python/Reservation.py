class Reservation:
  def __init__(self, observation_start, observation_end, observed_object, antenna_location):
    self.booking_date= #Now
    self.observation_start= observation_start #Start Date
    self.observation_end= observation_end #End date
    self.observed_object= observed_object #Norad id
    self.antenna_location= antenna_location

  def isToObserve(self):
    #Compare Now and observation start
    if
    return True
    else
    return False

  def observe(self):
    #if is observable: get Azimuth/elev of the sat
