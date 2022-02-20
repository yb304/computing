from .geo import stations_within_radius
from .utils import sorted_by_key

def stations_level_over_threshold(stations, tol):
    return sorted_by_key(
           [(n, n.relative_water_level()) 
           for n in stations if n.relative_water_level != None 
           and n.relative_water_level() > tol], 
           1, 
           reverse = True)
