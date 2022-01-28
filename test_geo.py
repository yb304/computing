import sys
import random
import type_validation as tv

from floodsystem.station import MonitoringStation
from floodsystem.geo import stations_by_distance, stations_within_radius
from floodsystem.stationdata import build_station_list


_o_stations_by_distance = stations_by_distance
_o_stations_within_radius = stations_within_radius


def _i_stations_by_distance(stations, p):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(p, (tuple, [float, float]))
    ret = _o_stations_by_distance(stations, p)
    tv.assert_type(ret,
                   (list, (tuple, [MonitoringStation,
                                   ("and", [float, tv.non_neg_p])])))
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


stations_by_distance = _i_stations_by_distance
stations_within_radius = _i_stations_within_radius

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
    assert res_all == stations

    # When centre equals the coordinate of a station, that station should be included
    for s in stations:
        res = stations_within_radius(stations, s.coord, 0.01)
        assert s in res
