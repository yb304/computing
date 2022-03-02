import sys
import type_validation as tv
from type_specs import rel_level_p, nat_int_p
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations
import test_station

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

    # cannot be more stations than input or limit N.
    # may be less due to absence of relative water level data
    assert len(stns) <= min(len(stations), 10)

    prev_level = sys.float_info.max
    for s in stns:
        rel_level = s.relative_water_level()
        assert s.typical_range_consistent()
        assert s.relative_water_level() is not None
        # sorted in descending order by relative level
        assert prev_level >= rel_level
        prev_level = rel_level

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
    # len(input) = 0
    stations_highest_rel_level(stations, 0)
    # 0 < len(input) < N
    stations_highest_rel_level(stations[:5], 10)
    # len(input) > N > 0
    stations_highest_rel_level(stations, 10)
    # N = 0, len(input) > 0
    stations_highest_rel_level(stations, 0)

    # rel. level = None
    nrls = test_station.new_sample_station()
    res = stations_highest_rel_level([nrls], 10)
    assert len(res) == 0

    # all inconsistent input => no output
    ntrs = test_station.new_sample_station_no_typ_range()
    res = stations_highest_rel_level([ntrs], 10)
    assert len(res) == 0
