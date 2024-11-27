import setup
#import test2
from skyfield.api import EarthSatellite, Topos, load
from skyfield.iokit import parse_tle_file
from skyfield.api import wgs84
import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import datetime 

def plot_altaz_positions(dates, altitudes, azimuths):
    """
    Plot satellite positions based on altitude and azimuth.

    Parameters:
    - dates: List of datetime objects representing observation times.
    - altitudes: List of altitudes (elevations) in degrees.
    - azimuths: List of azimuths in degrees.
    """
    # Convert azimuths to radians for plotting
    azimuths_rad = np.radians(azimuths)
    
    # Altitude determines the radius, with 90° (zenith) at the center and 0° (horizon) on the perimeter
    altitudes_normalized = [90 - alt for alt in altitudes]  # Invert for plotting

    # Create polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    
    # Assign colors to each point
    colors = plt.cm.jet(np.linspace(0, 1, len(dates)))  # Use a color map (jet) for distinct colors

    # Plot each satellite position as a discrete point
    scatter_plots = []
    for i in range(len(dates)):
        scatter_plot = ax.scatter(azimuths_rad[i], altitudes_normalized[i], c=[colors[i]], marker='o', s=100)
        scatter_plots.append(scatter_plot)
    
    # Configure the plot
    ax.set_theta_zero_location("N")  # North at the top
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_rlim(0, 90)  # Altitude range (90° at center to 0° on edge)
    ax.set_yticks([30, 60, 90])  # Radial ticks
    ax.set_yticklabels(['60°', '30°', 'Horizon'])  # Radial labels
    
    # Title
    ax.set_title("Satellite Positions in the Sky", va='bottom')

    # Add the legend outside the plot with the corresponding date for each point
    labels = [format_datetime(date) for date in dates]
    ax.legend(scatter_plots, labels, loc='center left', bbox_to_anchor=(1.05, 0.5))

    # Show the plot
    plt.show()

def convert_DTDate_to_isoDate(DTDate) :

    ts = load.timescale()
    time_obj = ts.tt(DTDate)
    print(time_obj.utc_iso())
    return time_obj.utc_iso()

def split_number(input):
    
    number = input.split('=')[1].split('>')[0]
    print(number)
    return number

def format_datetime(iso_datetime):
    
    # Convert the ISO datetime string to a datetime object
    dt_obj = datetime.fromisoformat(iso_datetime.replace("Z", ""))
    
    # Format the datetime object into the desired format
    return dt_obj.strftime('%Y-%m-%dT%H:%M:%S')

# Example data
ts=load.timescale()
current_time = ts.now()
DTDate = [current_time.tt + i * 0.002 for i in range(4)] 

# Convert Julian Dates to datetime
dates = [convert_DTDate_to_isoDate(tt) for tt in DTDate]

altitudes = [45, 60, 90, 30]  # Altitudes in degrees
azimuths = [90, 120, 270, 300]  # Azimuths in degrees

'''print(ts.now())
DTDate = split_number(ts.now())
#DTDate = [2460641.45440624, 2460641.45640624, 2460641.45840624, 2460641.46040624]

dates = convert_DTDate_to_isoDate(DTDate)
# Example data
dates = [
    "2024-11-26T00:00:00",
    "2024-11-26T00:02:00",
    "2024-11-26T00:04:00",
    "2024-11-26T00:06:00"
]#convert_DTDate_to_isoDate(test2.t)
altitudes = [45, 60, 30, 50] #test2.alt_sat  # Altitudes in degrees
azimuths = [90, 120, 270, 45]#test2.az_sat  # Azimuths in degrees'''

plot_altaz_positions(dates, altitudes, azimuths)
