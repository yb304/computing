# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""


class MonitoringStation:
    """This class represents a river level monitoring station"""

    def __init__(self, station_id, measure_id, label, coord, typical_range,
                 river, town):

        self.station_id = station_id
        self.measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self.name = label
        if isinstance(label, list):
            self.name = label[0]

        self.coord = coord
        self.typical_range = typical_range
        self.river = river
        self.town = town

        self.latest_level = None

    def __repr__(self):
        d = "Station name:     {}\n".format(self.name)
        d += "   id:            {}\n".format(self.station_id)
        d += "   measure id:    {}\n".format(self.measure_id)
        d += "   coordinate:    {}\n".format(self.coord)
        d += "   town:          {}\n".format(self.town)
        d += "   river:         {}\n".format(self.river)
        d += "   typical range: {}\n".format(self.typical_range)
        d += "   latest level:  {}".format(self.latest_level)
        return d

    def typical_range_consistent(self):
        """
        return false for range with no data or high point is lower than low point of river

        """
        return not (self.typical_range is None
                    or self.typical_range[0] > self.typical_range[1])

    def relative_water_level(self):
        """
        Returns the latest water level as a fraction of the typical range.
        None is returned if the typical range data is inconsistent or
        if the latest water level data is not available.

        Consider calling `stationdata.update_water_levels` first.

        Examples:
          water level == typical high:
            returns 1.0
          water level == typical low:
            returns 0.0
        """
        if not self.typical_range_consistent() or self.latest_level is None:
            return None
        else:
            return (self.latest_level - self.typical_range[0]) / (
                self.typical_range[1] - self.typical_range[0])


def inconsistent_typical_range_stations(stations):
    """
    Args:
      stations: list of MonitoringStation objects
    Returns:
      list of stations with inconsistent data
    """
    return [n for n in stations if not n.typical_range_consistent()]
