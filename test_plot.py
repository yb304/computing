import matplotlib.pyplot as plt
import type_validation as tv
from type_specs import rel_level_p, nat_int_p
from floodsystem.stationdata import build_station_list
from floodsystem.station import MonitoringStation
from datetime import datetime
from floodsystem.plot import plot_water_levels_no_show, plot_water_level_with_fit
from test_analysis import sample_dates, sample_dates2, sample_levels, sample_levels2

_o_plot_water_levels_no_show = plot_water_levels_no_show
_o_plot_water_level_with_fit = plot_water_level_with_fit


def _i_plot_water_levels_no_show(station, dates, levels):
    tv.assert_type(station, MonitoringStation)
    tv.assert_type(dates, (list, datetime))
    tv.assert_type(levels, (list, rel_level_p))
    return _o_plot_water_levels_no_show(station, dates, levels)


def _i_plot_water_level_with_fit(station, dates, levels, p):
    tv.assert_type(station, MonitoringStation)
    tv.assert_type(dates, (list, datetime))
    tv.assert_type(levels, (list, rel_level_p))
    tv.assert_type(p, nat_int_p)
    return _o_plot_water_level_with_fit(station, dates, levels, p)


plot_water_levels_no_show = _i_plot_water_levels_no_show
plot_water_level_with_fit = _i_plot_water_level_with_fit

stations = build_station_list()


def test_plot_water_levels():
    # should not throw errors
    plot_water_levels_no_show(stations[0], [], [])
    plot_water_levels_no_show(stations[0], sample_dates, sample_levels)
    plt.clf()


def test_plot_water_level_with_fit():
    # test for no errors
    plot_water_level_with_fit(stations[0], sample_dates2, sample_levels2, 4)
    plt.clf()
