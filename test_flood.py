from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations

stations = build_station_list()
update_water_levels(stations)

def test_stations_level_over_threshold():
    list1 = stations_level_over_threshold(stations, 0.8)
    for n in list1:
        assert n[1] > 0.8
        assert list1[n][1] <= list1[n-1][1]

def test_stations_highest_rel_level():
    list2 = stations_highest_rel_level(stations, 10)
    assert len(list2) == min(stations, 10)
    for n in list2:
        assert list2[n][1] <= list2[n-1][1]
    
    assert list2.typical_range_consistent()