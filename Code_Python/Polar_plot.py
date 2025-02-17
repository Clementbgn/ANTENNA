from skyfield.api import load, EarthSatellite, wgs84
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from Antenna_Site import antenna_site
from visibility_periods import is_visible, find_visibility_periods

# Import TLE Coordinates (Two-Line Element set for the satellite)

"""# These are used to calculate the satellite's position in orbit
tle_line1 = "1 25544U 98067A   23012.21574889  .00016717  00000-0  10270-3 0  9007"
tle_line2 = "2 25544  51.6434 296.1377 0005793  45.6760 314.4768 15.49912376389561"
satellite = EarthSatellite(tle_line1, tle_line2, "ISS (Zarya)", load.timescale())
"""
# Observation time set by the user (UTC time)
observation_year = 2025
observation_month = 1
observation_day = 12
observation_hour = 14
observation_minute = 5

# Load timescale and define the observation time
ts = load.timescale()
observation_time = ts.utc(observation_year, observation_month, observation_day, observation_hour, observation_minute)

# Check if the satellite is visible at the observation time
visible, az, el = is_visible(satellite, antenna_site, observation_time)
print(visible)


# Find visibility periods
last_period, current_period, next_period = find_visibility_periods(satellite, antenna_site, observation_time)

# Display results
if visible:
    print(f"At {observation_time.utc_iso()}, the satellite is visible.")
    print(f"Position: Azimuth = {az:.2f}°, Elevation = {el:.2f}°")
else:
    print(f"At {observation_time.utc_iso()}, the satellite is not visible.")
if last_period:
    print(f"Last visible period: {last_period[0].utc_iso()} to {last_period[1].utc_iso()}")
if next_period:
    print(f"Next visible period: {next_period[0].utc_iso()} to {next_period[1].utc_iso()}")
if current_period:
    print(f"Current visible period: {current_period[0].utc_iso()} to {current_period[1].utc_iso()}")

# Plot results
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
ax.set_theta_zero_location('N')  # North is at the top of the plot
ax.set_theta_direction(-1)  # Azimuth increases clockwise
ax.set_rlim(90, 0)  # Elevation: 90° at the horizon, 0° at the zenith

# Plot visibility periods
for period, label, color in [(last_period, "Last period", 'orange'), 
                             (current_period, "Current period", 'red'),
                             (next_period, "Next period", 'blue')]:
    if period:
        period_start = period[0].utc_datetime()  # Convert to datetime for iteration
        period_end = period[1].utc_datetime()
        interval_seconds = 60  # Time step for plotting (60 seconds)

        period_times = []
        current_time = period_start
        while current_time <= period_end:
            period_times.append(ts.utc(current_time.year, current_time.month, current_time.day,
                                       current_time.hour, current_time.minute, current_time.second))
            current_time += timedelta(seconds=interval_seconds)

        period_azimuths = []
        period_elevations = []
        for t in period_times:
            _, azimuth, elevation = is_visible(satellite, antenna_site, t)
            period_azimuths.append(np.radians(azimuth))
            period_elevations.append(elevation)

        # Plot the visibility curve
        ax.plot(period_azimuths, period_elevations, label=label, color=color)

# Plot the satellite's current position if visible
if visible:
    ax.scatter(np.radians(az), el, color='red', label="Current position", zorder=5)

# Add title and legend
ax.set_title("Satellite trajectory seen from the ground station", va='bottom')
ax.legend(loc='lower left')
plt.show()
