# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import MonitoringStation
from floodsystem.station import inconsistent_typical_range_stations
import type_validation as tv

_o_inconsistent_typical_range_stations = inconsistent_typical_range_stations


def _i_inconsistent_typical_range_stations(stations):
    tv.assert_type(stations, (list, MonitoringStation))
    ret = _o_inconsistent_typical_range_stations(stations)
    tv.assert_type(ret, (list, MonitoringStation))
    return ret


inconsistent_typical_range_stations = _i_inconsistent_typical_range_stations


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

    # Create a station
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
