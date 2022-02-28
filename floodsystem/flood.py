from .utils import sorted_by_key
from .station import MonitoringStation

def stations_level_over_threshold(stations, tol):
    return sorted_by_key(
           [(station, station.relative_water_level()) 
           for station in stations if station.relative_water_level() != None 
           and station.relative_water_level() > tol], 
           1, 
           reverse = True)

def stations_highest_rel_level(stations, N):
    return sorted_by_key(
           [(station, station.relative_water_level()) 
           for station in stations if station.relative_water_level() != None],
           reverse=True)[:N]

