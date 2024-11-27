from skyfield.api import load, Topos,EarthSatellite
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

'''def plot_satellite_view(tle_lines, ground_station_lat, ground_station_lon):
    # Load the satellite from TLE
    satellite = EarthSatellite(tle_lines[1], tle_lines[2], tle_lines[0])
    ts = load.timescale()
    
    # Define the ground station location
    ground_station = Topos(latitude_degrees=ground_station_lat, longitude_degrees=ground_station_lon)
    
    # Define the time range for the trajectory (next 10 minutes)
    time_now = ts.now()
    time_range = [time_now + timedelta(seconds=i * 30) for i in range(20)]  # 30s intervals
    
    # Calculate satellite positions
    altitudes = []
    azimuths = []
    for time in time_range:
        difference = satellite - ground_station
        topocentric = difference.at(time)
        alt, az, _ = topocentric.altaz()
        altitudes.append(alt.degrees)
        azimuths.append(az.degrees)
    
    # Plot the visualization
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    
    # Convert azimuths to radians for plotting
    azimuths_rad = np.radians(azimuths)
    
    # Altitude determines the radius, with 90° (zenith) at the center and 0° (horizon) on the perimeter
    altitudes_normalized = [90 - alt for alt in altitudes]  # Invert for plotting
    
    # Plot the satellite trajectory
    ax.plot(azimuths_rad, altitudes_normalized, 'r--', label="Satellite Trajectory")
    
    # Plot the current satellite position
    ax.plot(azimuths_rad[0], altitudes_normalized[0], 'bo', label="Current Position")
    
    # Configure the plot
    ax.set_theta_zero_location("N")  # North at the top
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_rlim(0, 90)  # Altitude range (90° at center to 0° on edge)
    ax.set_yticks([30, 60, 90])  # Radial ticks
    ax.set_yticklabels(['60°', '30°', 'Horizon'])  # Radial labels
    ax.legend()
    ax.set_title("Satellite Position as Seen from Ground Station", va='bottom')

    # Show the plot
    plt.show()

# Example usage
tle_lines = [
    "ISS (ZARYA)",
    "1 25544U 98067A   24331.51835648  .00001587  00000+0  37106-4 0  9990",
    "2 25544  51.6447  63.4478 0006984  90.9458 269.2457 15.50099717398414"
]

ground_station_lat = 37.7749  # Example: San Francisco, CA
ground_station_lon = -122.4194

plot_satellite_view(tle_lines, ground_station_lat, ground_station_lon)
'''

def convert_DTDate_to_isoDate(DTDate):
    ts = load.timescale()
    time_obj = ts.tt(DTDate)  # Create Skyfield Time object from Julian Date
    iso_date = time_obj.utc_iso()  # Get the ISO string representation
    print("ISO Date:", iso_date)  # This is the Julian Date in ISO-like format
    return iso_date

# Function to manually format and convert the Julian Date to Gregorian Date
def julian_to_gregorian(julian_date):
    ts = load.timescale()
    time_obj = ts.tt(julian_date)  # Convert the Julian date to a Skyfield Time object
    return time_obj.utc_iso()  # This returns a Julian Date in a more readable format

# Function to convert Julian Date to a proper datetime format
def format_datetime(iso_datetime):
    # Remove the 'Z' (UTC indicator) and convert to datetime object
    iso_datetime = iso_datetime.replace('Z', '')  # Remove 'Z'
    dt_obj = datetime.fromisoformat(iso_datetime)  # Convert to datetime object
    return dt_obj.strftime('%Y-%m-%dT%H:%M:%S')  # Format the datetime

# Example: Let's use the current time and generate a list of Julian Dates
ts = load.timescale()
current_time = ts.now()  # Get current Julian Date
DTDate = [current_time.tt + i * 0.002 for i in range(4)]  # Generate a few Julian Dates

# Convert the Julian Dates to ISO formatted strings and then to datetime
dates = [convert_DTDate_to_isoDate(tt) for tt in DTDate]
formatted_dates = [format_datetime(date) for date in dates]

# Print the formatted dates
print("Formatted Dates:")
for date in formatted_dates:
    print(date)