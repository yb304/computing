import sys
import type_validation as tv
from type_specs import rel_level_p
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations
from datetime import datetime, timedelta
from floodsystem.plot import plot_water_levels, plot_water_levels_no_show


enable_plot_tests = False

_o_plot_water_levels_no_show = plot_water_levels_no_show
_o_plot_water_levels = plot_water_levels


def _i_plot_water_levels_no_show(station, dates, levels):
    tv.assert_type(station, MonitoringStation)
    tv.assert_type(dates, (list, datetime))
    tv.assert_type(levels, (list, rel_level_p))
    _o_plot_water_levels_no_show(station, dates, levels)


def _i_plot_water_levels(station, dates, levels):
    tv.assert_type(station, MonitoringStation)
    tv.assert_type(dates, (list, datetime))
    tv.assert_type(levels, (list, rel_level_p))
    _o_plot_water_levels(station, dates, levels)



# plot_water_levels_no_show = _i_plot_water_levels_no_show
plot_water_levels = _i_plot_water_levels


stations = build_station_list()

sample_times = [datetime(2016, 12, 30), datetime(2016, 12, 31), datetime(2017, 1, 1),
                datetime(2017, 1, 2), datetime(2017, 1, 3), datetime(2017, 1, 4),
                datetime(2017, 1, 5)]

sample_levels = [0.2, 0.7, 0.95, 0.92, 1.02, 0.91, 0.64]


def test_plot_water_level():
    if not enable_plot_tests:
        return
    # should not throw errors
    plot_water_levels(stations[0], [], [])
    plot_water_levels(stations[0], sample_times, sample_levels)
