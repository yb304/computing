# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

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
    # TODO
    return None
