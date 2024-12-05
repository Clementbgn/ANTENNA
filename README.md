# Missions principales

**1/** Mission Analysis: Creation of a module to generate orbit trajectories from TLE and computing visibility time, azimuth and elevation for a given earth station;

Pour le programme de suivi satellite, vous pouvez le diviser en deux: un pour la planification qui montre la prévision du contact et les valeurs de pointage, et un en temps-réel qui selon une réservation de passe active un suivi virtuel selon le temps du pc. Ça peut être au début simplement imprimer sur l'écran l'évolution du pointage Az/El.

**2/** RF Processing: Creation of a GNU radio module to interface with USRP/Pluto to acquire a signal and demodulate it;

## Status

- [x] Get TLE for any Satellite knowing Norad_Id
- [x] Detect visibility Time under a specific Delta T for a specific location

## Todo
- [ ] Azimuth + Elevation
- [ ] RA + Dec

- [ ] GNU  Radio modules : *TO develop*

## Libraries

![alt text](https://rhodesmill.org/skyfield/_static/logo.png)