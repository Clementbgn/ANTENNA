#IMPORTS
import astropy.coordinates
import pyorbital
from pyorbital.orbital import Orbital
import numpy as np
import datetime
import time
import astropy
import astropy.units as u
import pandas as pd

# Use current TLEs from the internet: need to edit the file platforms.txt add [Name sat id_norad]
orb = Orbital("EIRSAT-1")

#Set a deltaT for the calculation of the propagation
delta1s=datetime.timedelta(seconds=1)

#Definition of the Now time in UTC
now = datetime.datetime.now(datetime.timezone.utc)

#Creation of a dynamic list
table = []

#Propagate the orbit for the next t_prop seconds

t_prop = 600 #s
for x in range(0, t_prop):
    coord=np.array(orb.get_lonlatalt(now))
    table.append(coord) #Addition of the x second propagation to the table
    now=now+delta1s #Incrementation of the time
    #print(table[x]) #Display table as the for loop go

table=np.array(table) #List conversion to array table[index of delta T's][0=Lon 1=LAt 2=Alt]

#Convert LongLatAlt to Ra dec

long = np.deg2rad(table[:,0])
lat = np.deg2rad(table[:,1])
alt = table[:,2]*1000

Position_geocentric = astropy.coordinates.SkyCoord(long, lat, alt, frame='geocentricmeanecliptic', unit=(u.radian, u.radian, u.meter))
Position_j2000 = Position_geocentric.transform_to('fk5')
Table_j2000 = Position_j2000.to_table()
Table_j2000.remove_column("distance")

print(Table_j2000) #Not working yet








'''
for x in range (0, int(table.size/3)):
    y=0

    long=np.deg2rad(table[x][y])
    lat=np.deg2rad(table[x][y+1])
    alt=table[x][y+2]
    Position_geocentric = astropy.coordinates.SkyCoord(long, lat, alt, frame='geocentricmeanecliptic', unit=(u.radian, u.radian, u.meter))
    Position_j2000 = Position_geocentric.transform_to('fk5')
    Table_ra_dec.append(Position_j2000)

Table_ra_dec = np.array(Table_ra_dec)
'''