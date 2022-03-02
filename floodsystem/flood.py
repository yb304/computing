from .utils import sorted_by_key
from .station import MonitoringStation


def stations_level_over_threshold(stations, tol):
    tuples = map(lambda s: (s, s.relative_water_level()), stations)
    filtered_tuples = filter(lambda t:
                             t[1] is not None and t[1] > tol,
                             tuples)
    sorted_tuples = list(sorted_by_key(filtered_tuples, 1, reverse=True))
    print(sorted_tuples[:10])
    return sorted_tuples


def stations_highest_rel_level(stations, N):
    stations_with_level = [(station, station.relative_water_level())
                           for station in stations
                           if station.relative_water_level() is not None]

    # [(Station1, 2.4), (Station2, 4.2)]
    sorted_stations_with_level = sorted_by_key(stations_with_level,
                                               1,
                                               reverse=True)[:N]

    # [Station1 , Station2]
    sorted_stations = [t[0] for t in sorted_stations_with_level]
    return sorted_stations
