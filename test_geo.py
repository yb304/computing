import sys
import random
from functools import reduce
import type_validation as tv


from floodsystem.station import MonitoringStation
from floodsystem.geo import \
    stations_by_distance, stations_within_radius, rivers_with_station, stations_by_river, rivers_by_station_number
from floodsystem.stationdata import build_station_list

_o_stations_by_distance = stations_by_distance
_o_stations_within_radius = stations_within_radius
_o_rivers_with_station = rivers_with_station
_o_stations_by_river = stations_by_river
_o_rivers_by_station_number = rivers_by_station_number


def _i_stations_by_distance(stations, p):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(p, (tuple, [float, float]))
    ret = _o_stations_by_distance(stations, p)
    tv.assert_type(
        ret,
        (list, (tuple, [MonitoringStation, ("and", [float, tv.non_neg_p])])))
    assert len(ret) == len(stations)

    # Ascending order
    last_dist = 0
    for station, dist in ret:
        assert last_dist <= dist
        last_dist = dist

    return ret


def _i_stations_within_radius(stations, centre, r):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(centre, (tuple, [float, float]))
    tv.assert_type(r, ("and", [float, tv.non_neg_p]))
    ret = _o_stations_within_radius(stations, centre, r)
    tv.assert_type(ret, (list, MonitoringStation))
    assert len(ret) <= len(stations)

    return ret


def _i_rivers_with_station(stations):
    tv.assert_type(stations, (list, MonitoringStation))
    ret = _o_rivers_with_station(stations)
    tv.assert_type(ret, (set, tv.non_empty_str_spec))
    return ret


def _i_stations_by_river(stations):
    tv.assert_type(stations, (list, MonitoringStation))
    ret = _o_stations_by_river(stations)
    tv.assert_type(ret, (dict, tv.non_empty_str_spec,
                         ("and", [(list, MonitoringStation),
                                  (lambda l: len(l) > 0)])))
    return ret


def _i_rivers_by_station_number(stations, N):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(N, ("and", [int, tv.non_neg_p]))
    ret = _o_rivers_by_station_number(stations, N)
    tv.assert_type(
        ret, (list,
              (tuple, [tv.non_empty_str_spec,
                       ("and", [int, lambda x: x > 0])])))
    # number of rivers should be smaller or equal to the number of stations
    assert len(ret) <= len(stations)
    for river in ret[N:]:
        assert river[1] == ret[N - 1][1]
    return ret


stations_by_distance = _i_stations_by_distance
stations_within_radius = _i_stations_within_radius
rivers_with_station = _i_rivers_with_station
stations_by_river = _i_stations_by_river
rivers_by_station_number = _i_rivers_by_station_number

stations = build_station_list()


def test_stations_by_distance():
    # Zero distance when coordinate equals a station's coordinate
    for s in random.sample(stations, 10):
        results = stations_by_distance(stations, s.coord)
        for r in results:
            if r[0] == s:
                assert round(r[1], 8) == 0
                break

    stations_by_distance(list(reversed(stations)), (-100., 100.))
    stations_by_distance([], (0., 0.))


def test_stations_within_radius():
    # If radius is zero, there should be no results
    res_empty = stations_within_radius(stations, (0., 0.), 0.)
    assert res_empty == []

    # If a large radius is given, all stations should be included
    res_all = stations_within_radius(stations, (0., 0.), sys.float_info.max)
    assert set(res_all) == set(stations)

    # When centre equals the coordinate of a station, that station should be included
    for s in random.sample(stations, 10):
        res = stations_within_radius(stations, s.coord, 0.01)
        assert s in res


def test_rivers_with_station():
    assert set() == rivers_with_station([])
    for i in range(10):
        sample = random.sample(stations, random.randint(1, 20))
        rivers = rivers_with_station(sample)
        assert len(rivers) > 0
        assert len(rivers) <= len(sample)


def test_stations_by_river():
    sbr = stations_by_river(stations)
    ret_stations = reduce(lambda acc, sl: acc + sl, sbr.values(), [])
    ret_stations_set = set(ret_stations)
    # no duplicate stations
    assert len(ret_stations) == len(ret_stations_set)
    # no missing stations
    assert set(stations) == ret_stations_set
    # all rivers included
    ret_rivers = set(sbr.keys())
    assert ret_rivers == rivers_with_station(stations)


def test_rivers_by_station_number():
    rivers_by_station_number(stations, len(stations))
    rivers_by_station_number(stations, 9)
    assert [] == rivers_by_station_number([], 9)
