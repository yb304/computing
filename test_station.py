# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

import type_validation as tv
from floodsystem.station import (MonitoringStation,
                                 inconsistent_typical_range_stations)
from floodsystem.stationdata import build_station_list
from type_specs import rel_level_p


_o_inconsistent_typical_range_stations = inconsistent_typical_range_stations
_o_relative_water_level = MonitoringStation.relative_water_level


def _i_inconsistent_typical_range_stations(stations):
    tv.assert_type(stations, (list, MonitoringStation))
    ret = _o_inconsistent_typical_range_stations(stations)
    tv.assert_type(ret, (list, MonitoringStation))
    return ret


def _i_relative_water_level(self):
    rwl = _o_relative_water_level(self)
    tv.assert_type(rwl, ("maybe", rel_level_p))
    if not self.typical_range_consistent():
        assert rwl is None
    return rwl


inconsistent_typical_range_stations = _i_inconsistent_typical_range_stations
MonitoringStation.relative_water_level = _i_relative_water_level

stations = build_station_list()


def new_sample_station():
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    return MonitoringStation(s_id, m_id, label, coord, trange, river, town)


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


def new_sample_station_no_typ_range():
    ntrs = new_sample_station()
    ntrs.label = "no station"
    ntrs.typical_range = None
    return ntrs


def test_inconsistent_typical_range_stations():
    ntrs = new_sample_station_no_typ_range()

    wrs = new_sample_station()
    wrs.label = "wrong range of stations"
    wrs.typical_range = (2.3, -3.4445)

    s = new_sample_station()

    assert (inconsistent_typical_range_stations([ntrs, wrs, s]) == [ntrs, wrs])
    assert [] == inconsistent_typical_range_stations([])
    assert s.typical_range_consistent()
    assert not ntrs.typical_range_consistent()
    assert not wrs.typical_range_consistent()


def test_relative_water_level():
    s = new_sample_station()

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
