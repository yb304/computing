import sys
import type_validation as tv
from type_specs import rel_level_p, nat_int_p
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations


_o_stations_level_over_threshold = stations_level_over_threshold
_o_stations_highest_rel_level = stations_highest_rel_level


def _i_stations_level_over_threshold(stations, tol):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(tol, rel_level_p)
    stns = _o_stations_level_over_threshold(stations, tol)
    tv.assert_type(stns, (list, (tuple, [MonitoringStation, rel_level_p])))
    return stns


def _i_stations_highest_rel_level(stations, N):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(N, nat_int_p)
    stns = _o_stations_highest_rel_level(stations, N)
    tv.assert_type(stns, (list, MonitoringStation))
    return stns


stations_level_over_threshold = _i_stations_level_over_threshold
stations_highest_rel_level = _i_stations_highest_rel_level

stations = build_station_list()
update_water_levels(stations)


def test_stations_level_over_threshold():
    def test_for_tol(threshold):
        stns_over_tol = stations_level_over_threshold(stations, threshold)
        assert len(stns_over_tol) <= len(stations)

        prev_level = sys.float_info.max
        for s, rel_level in stns_over_tol:
            assert rel_level > threshold
            # Test descending order by relative level
            assert rel_level <= prev_level
            prev_level = rel_level

    test_for_tol(0.)
    test_for_tol(0.5)
    test_for_tol(1.)


def test_stations_highest_rel_level():
    list2 = stations_highest_rel_level(stations, 10)
    assert len(list2) == min(stations, 10)
    for n in list2:
        assert list2[n][1] <= list2[n - 1][1]

    assert list2.typical_range_consistent()
