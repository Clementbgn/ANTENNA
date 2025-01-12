import Reservation
import Satellite_Loader
import Antenna_Site
ts = Reservation.ts

Reservation1= Reservation.Reservation(ts,
                                      ts.utc(2025,1,12,19,20,0), 
                                      ts.utc(2025, 1, 12, 21, 0, 0),
                                      Satellite_Loader.satellite,
                                      Antenna_Site.antenna_site)

print(Reservation1.isToObserve())