import Reservation
import Satellite_list
import Antenna_Site
ts = Reservation.ts

EIRSAT_Obs1 = Reservation.Reservation(ts,
                                      ts.utc(2025,1,12,19,20,0), 
                                      ts.utc(2025, 1, 12, 21, 0, 0),
                                      Satellite_list.Satellites[0],
                                      Antenna_Site.antenna_site)


print(EIRSAT_Obs1.isToObserve())