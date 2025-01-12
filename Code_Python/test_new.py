from skyfield.api import load, EarthSatellite, wgs84
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

# Charger les données TLE
tle_line1 = "1 25544U 98067A   23012.21574889  .00016717  00000-0  10270-3 0  9007"
tle_line2 = "2 25544  51.6434 296.1377 0005793  45.6760 314.4768 15.49912376389561"
satellite = EarthSatellite(tle_line1, tle_line2, "ISS (Zarya)", load.timescale())

# Station sol
station_lat = 48.8566  # Latitude de Paris
station_lon = 2.3522   # Longitude de Paris
station_alt = 0.035    # Altitude en km
station = wgs84.latlon(station_lat, station_lon, station_alt)

# Temps d'observation
observation_year = 2025
observation_month = 1
observation_day = 12
observation_hour = 13
observation_minute = 30

ts = load.timescale()
observation_time = ts.utc(observation_year, observation_month, observation_day, observation_hour, observation_minute)

# Vérification de la visibilité
def is_visible(satellite, station, time):
    difference = satellite - station
    topocentric = difference.at(time)
    alt, az, _ = topocentric.altaz()
    return alt.degrees > 0, az.degrees, alt.degrees

visible, az, el = is_visible(satellite, station, observation_time)

# Trouver la dernière et la prochaine période
def find_visibility_periods(satellite, station, observation_time, search_duration_minutes=720):
    step_minutes = 1  # Pas d'une minute
    duration = range(-search_duration_minutes, search_duration_minutes, step_minutes)

    last_period = None
    next_period = None
    current_period = []
    for delta in duration:
        t = observation_time + timedelta(minutes=delta)
        vis, _, _ = is_visible(satellite, station, t)

        if vis:
            if not current_period:
                current_period.append(t)
        else:
            if current_period and len(current_period) == 1:
                current_period.append(t)
                if t < observation_time:
                    last_period = current_period
                elif t > observation_time and next_period is None:
                    next_period = current_period
                current_period = []

    return last_period, next_period

last_period, next_period = find_visibility_periods(satellite, station, observation_time)

# Affichage des résultats
if visible:
    print(f"À {observation_time.utc_iso()}, le satellite est visible.")
    print(f"Position : Azimut = {az:.2f}°, Élévation = {el:.2f}°")
else:
    print(f"À {observation_time.utc_iso()}, le satellite n'est pas visible.")
    if last_period:
        print(f"Dernière période visible : {last_period[0].utc_iso()} à {last_period[1].utc_iso()}")
    if next_period:
        print(f"Prochaine période visible : {next_period[0].utc_iso()} à {next_period[1].utc_iso()}")

# Affichage graphique polaire
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
ax.set_theta_zero_location('N')  # Le nord en haut
ax.set_theta_direction(-1)  # Sens horaire pour l'azimut
ax.set_rlim(90, 0)  # 90° à l'extérieur (horizon), 0° au centre (zénith)

# Tracé des périodes adjacentes
for period, label in [(last_period, "Dernière période"), (next_period, "Prochaine période")]:
    if period:
        period_start = period[0].utc_datetime()
        period_end = period[1].utc_datetime()
        interval_seconds = 60  # Intervalle de 60 secondes

        period_times = []
        current_time = period_start
        while current_time <= period_end:
            period_times.append(ts.utc(current_time.year, current_time.month, current_time.day,
                                       current_time.hour, current_time.minute, current_time.second))
            current_time += timedelta(seconds=interval_seconds)

        period_azimuths = []
        period_elevations = []
        for t in period_times:
            _, azimuth, elevation = is_visible(satellite, station, t)
            period_azimuths.append(np.radians(azimuth))
            period_elevations.append(elevation)

        ax.plot(period_azimuths, period_elevations, label=label)

# Position actuelle
if visible:
    ax.scatter(np.radians(az), el, color='red', label="Position actuelle", zorder=5)

ax.set_title("Trajectoire du satellite vu depuis la station sol", va='bottom')
ax.legend(loc='lower left')
plt.show()
