from skyfield.api import load, EarthSatellite, wgs84
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from Antenna_Site import antenna_site

# Import TLE Coordinates (Two-Line Element set for the satellite)
# These are used to calculate the satellite's position in orbit
tle_line1 = "1 25544U 98067A   23012.21574889  .00016717  00000-0  10270-3 0  9007"
tle_line2 = "2 25544  51.6434 296.1377 0005793  45.6760 314.4768 15.49912376389561"
satellite = EarthSatellite(tle_line1, tle_line2, "ISS (Zarya)", load.timescale())

# Observation time set by the user (UTC time)
observation_year = 2025
observation_month = 1
observation_day = 12
observation_hour = 14
observation_minute = 5

# Load timescale and define the observation time
ts = load.timescale()
observation_time = ts.utc(observation_year, observation_month, observation_day, observation_hour, observation_minute)

# Function to determine if the satellite is visible from the ground station
def is_visible(satellite, antenna_site, time):
    """
    Determine if the satellite is visible from the ground station at a given time.
    :param satellite: The EarthSatellite object representing the satellite
    :param station: The wgs84 object representing the ground station
    :param time: The time of observation (Skyfield Time object)
    :return: (visibility status, azimuth, elevation)
    """
    difference = satellite - antenna_site  # Relative position between satellite and station
    topocentric = difference.at(time)  # Topocentric (local) position of the satellite
    alt, az, _ = topocentric.altaz()  # Altitude (elevation) and azimuth angles
    return alt.degrees > 0, az.degrees, alt.degrees  # Visible if elevation > 0 degrees

# Check if the satellite is visible at the observation time
visible, az, el = is_visible(satellite, antenna_site, observation_time)

# Function to find the last, current, and next visibility periods
def find_visibility_periods(satellite, station, observation_time, search_duration_minutes=720):
    """
    Find the last, current, and next visibility periods of the satellite.
    :param satellite: The EarthSatellite object
    :param station: The wgs84 object representing the ground station
    :param observation_time: The observation time (Skyfield Time object)
    :param search_duration_minutes: Duration to search for visibility periods (default: 720 minutes)
    :return: (last_period, current_period, next_period)
    """
    step_minutes = 1  # Time step (in minutes)
    duration = range(-search_duration_minutes, search_duration_minutes, step_minutes)

    last_period = None
    current_period = None
    next_period = None
    period_in_progress = False

    for delta in duration:
        t = observation_time + timedelta(minutes=delta)  # Time offset by delta
        vis, _, _ = is_visible(satellite, station, t)

        if vis:
            if not period_in_progress:  # Start of a new visibility period
                period_start = t
                period_in_progress = True
        else:
            if period_in_progress:  # End of a visibility period
                period_end = t
                period_in_progress = False

                # Classify the visibility period
                if period_start.utc_datetime() <= observation_time.utc_datetime() <= period_end.utc_datetime():
                    current_period = [period_start, period_end]  # Current visibility period
                elif period_end.utc_datetime() < observation_time.utc_datetime():
                    last_period = [period_start, period_end]  # Last visibility period
                elif period_start.utc_datetime() > observation_time.utc_datetime() and next_period is None:
                    next_period = [period_start, period_end]  # Next visibility period

    # Ensure there is always a next period, even if it is far in the future
    if next_period is None:
        future_time = observation_time + timedelta(minutes=30)
        next_period = [future_time, future_time + timedelta(minutes=10)]

    return last_period, current_period, next_period


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
