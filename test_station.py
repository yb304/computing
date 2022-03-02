# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import MonitoringStation
from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list
import type_validation as tv

_o_inconsistent_typical_range_stations = inconsistent_typical_range_stations
_o_relative_water_level = MonitoringStation.relative_water_level


def _i_inconsistent_typical_range_stations(stations):
    tv.assert_type(stations, (list, MonitoringStation))
    ret = _o_inconsistent_typical_range_stations(stations)
    tv.assert_type(ret, (list, MonitoringStation))
    return ret


def _i_relative_water_level(self):
    rwl = _o_relative_water_level(self)
    tv.assert_type(rwl, ("maybe", float))
    if not self.typical_range_consistent():
        assert rwl is None
    return rwl


inconsistent_typical_range_stations = _i_inconsistent_typical_range_stations
MonitoringStation.relative_water_level = _i_relative_water_level

stations = build_station_list()


def test_create_monitoring_station():
    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    assert s.station_id == s_id
    assert s.measure_id == m_id
    assert s.name == label
    assert s.coord == coord
    assert s.typical_range == trange
    assert s.river == river
    assert s.town == town


def test_inconsistent_typical_range_stations():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "no station"
    coord = (-2.0, 4.0)
    trange = None
    river = "River X"
    town = "My Town"
    ntrs = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "wrong range of stations"
    coord = (-2.0, 4.0)
    trange = (2.3, -3.4445)
    river = "River X"
    town = "My Town"
    wrs = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    assert (inconsistent_typical_range_stations([ntrs, wrs, s]) == [ntrs, wrs])
    assert [] == inconsistent_typical_range_stations([])
    assert s.typical_range_consistent()
    assert not ntrs.typical_range_consistent()
    assert not wrs.typical_range_consistent()


def test_relative_water_level():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    s.latest_level = None
    assert s.relative_water_level() is None

    # typ. low case
    s.latest_level = s.typical_range[0]
    assert round(s.relative_water_level(), 8) == 0.

    # typ. high case
    s.latest_level = s.typical_range[1]
    assert round(s.relative_water_level(), 8) == 1.

    # latest_level = typ range/2 → ret 0.5
    s.latest_level = (s.typical_range[0] + s.typical_range[1]) / 2
    assert round(s.relative_water_level(), 8) == 0.5

    # test on live data
    for ls in stations:
        ls.relative_water_level()
