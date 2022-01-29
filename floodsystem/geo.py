# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from math import haversine
from .utils import sorted_by_key  # noqa


def stations_by_distance(stations, p):
    """
    Args:
      stations: list of MonitoringStation objects
      p: (float, float); A coorinate
    Returns:
      A list of (station, distance) tuples, sorted by distance in ascending order.
      `distance` (float) is from the coordinate `p` to the station (MonitoringStation).
    """
    dists = map(lambda s: (s, haversine(s.coord, p)), stations)
    return sorted_by_key(dists, 1)


def stations_within_radius(stations, centre, r):
    # TODO
    return None


def stations_by_river(stations):
    """
    Groups stations by the river they are on.

    Args:
      stations: list of MonitoringStation objects
    Returns:
      A dictionary mapping river names (string) to a list of MonitoringStation objects
    """
    ret = {}
    for s in stations:
        river = s.river
        if river in ret:
            ret[river].append(s)
        else:
            ret[river] = [s]
    return ret

def rivers_by_station_number(stations, N):
  full_list = sorted_by_key([(key,len(value)) for key, value in stations_by_river(stations).items()], 1, reverse=True)
  new_list = full_list[:N]
  for i in range(N, len(full_list)):
    if full_list[i][1] < full_list[N-1][1]:
      break
    else:
      new_list.append(full_list[i])

  return new_list
