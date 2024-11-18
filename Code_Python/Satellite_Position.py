#IMPORTS
import pyorbital
import numpy as np
from pyorbital.orbital import Orbital
import datetime
import time
import json

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
    table.append(np.array(orb.get_lonlatalt(now))) #Addition of the x second propagation to the table
    now=now+delta1s #Incrementation of the time
    print(table[x]) #Display table as the for loop go





'''
#DEFINITION OF NOW: UTC timezone
now = datetime.datetime.now(datetime.timezone.utc)

#Obtention of Longitude Latitude and Altitude now
LongLatAlt = np.array(orb.get_lonlatalt(now))
print("Position Now: ")
print(LongLatAlt)

#creation of a deltaT
delta=datetime.timedelta(hours=1)

#Addition of the deltaT to t0(old now)
dans1h=now+delta

#Print Longitude Latitude and Altitude at now+deltaT
LongLatAlt1h = np.array(orb.get_lonlatalt(dans1h))
print("Position in 1 hour: ")
print(LongLatAlt1h)
'''