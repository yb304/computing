from .utils import sorted_by_key
from .station import MonitoringStation


def stations_level_over_threshold(stations, tol):
    return sorted_by_key(
        [(station, station.relative_water_level())
         for station in stations if station.relative_water_level() != None
         and station.relative_water_level() > tol],
        1,
        reverse=True)


def stations_highest_rel_level(stations, N):
    stations_with_level = [(station, station.relative_water_level())
        for station in stations
        if station.relative_water_level() != None]

    # [(Station1, 2.4), (Station2, 4.2)]
    sorted_stations_with_level = sorted_by_key(stations_with_level, 1, reverse=True)[:N]

    # [Station1 , Station2]
    #sorted_stations = [n[0] for n in sorted_stations_with_level]
    return sorted_stations_with_level
