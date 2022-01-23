from functools import partial
import operator as op
import type_validation as tv

from floodsystem.station import MonitoringStation
from floodsystem.geo import stations_by_distance
from floodsystem.stationdata import build_station_list


_o_stations_by_distance = stations_by_distance


def _i_stations_by_distance(stations, p):
    tv.assert_type(stations, (list, MonitoringStation))
    tv.assert_type(p, (tuple, [float, float]))
    ret = _o_stations_by_distance(stations, p)
    tv.assert_type(ret,
                   (list, (tuple, [MonitoringStation,
                                   ("and", [float,
                                            partial(op.le, 0)])])))
    assert len(ret) == len(stations)

    # Ascending order
    last_dist = 0
    for station, dist in ret:
        assert last_dist < dist
        last_dist = dist

    return ret


stations_by_distance = _i_stations_by_distance

stations = build_station_list()


def test_stations_by_distance():
    # Zero distance when coordinate equals a station's coordinate
    for s in stations:
        results = stations_by_distance(stations, s.coord)
        for r in results:
            if r[0] == s:
                assert round(r[1], 8) == 0
                break

    stations_by_distance(reversed(stations), (-100., 100.))
    stations_by_distance([], (0., 0.))
