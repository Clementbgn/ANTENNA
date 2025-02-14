from datetime import timedelta
import numpy as np


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

# Function to find the last, current, and next visibility periods
def find_visibility_periods(satellite, station, observation_time, search_duration_minutes=720):
    """
    Find the last, current, and next visibility periods of the satellite.
    :param satellite: The EarthSatellite object
    :param station: The wgs84 object representing the ground station
    :param observation_time: The observation time (Skyfield Time object)
    :param search_duration_minutes: Duration to search for visibility periods (default: 720 minutes = 12h)
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