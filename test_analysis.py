import sys
import type_validation as tv
import numpy as np
from type_specs import rel_level_p, nat_int_p
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations
from datetime import datetime, timedelta
from floodsystem.plot import plot_water_levels, plot_water_levels_no_show
from floodsystem.analysis import polyfit

_o_polyfit = polyfit


def _i_polyfit(dates, levels, p):
    tv.assert_type(dates, (list, datetime))
    tv.assert_type(levels, (list, rel_level_p))
    tv.assert_type(p, nat_int_p)
    ret = _o_polyfit(dates, levels, p)
    tv.assert_type(ret, (tuple, [np.poly1d, float]))
    return ret


polyfit = _i_polyfit

sample_dates = np.linspace(0, 2, 10)
sample_levels = [0.1, 0.09, 0.23, 0.34, 0.78, 0.74, 0.43, 0.31, 0.01, -0.05]


def test_polyfit():
    # no errors should be thrown
    polyfit(sample_dates, sample_levels, 1)
    polyfit(sample_dates, sample_levels, 2)
    polyfit(sample_dates, sample_levels, 3)
    polyfit(sample_dates, sample_levels, 4)
