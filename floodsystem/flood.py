from .utils import sorted_by_key


def stations_level_over_threshold(stations, tol):
    """
    Filters stations to get those with a relative water level above `tol`
    Args:
      stations: list of MonitoringStation objects
      tol: relative water level threshold (float)
    Returns:
      List of tuples of (station, relative water level)
      sorted in descending order by the relative water level
    """
    tuples = map(lambda s: (s, s.relative_water_level()), stations)
    filtered_tuples = filter(lambda t: t[1] is not None and t[1] > tol, tuples)
    sorted_tuples = list(sorted_by_key(filtered_tuples, 1, reverse=True))
    return sorted_tuples


def stations_highest_rel_level(stations, N):
    """
    Args:
      stations: list of MonitoringStation objects
      N: The maximum number of stations to return
    Returns:
      The filtered list of stations which have the N highest water levels
      relative to the typical range, in a descending order
    """
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
