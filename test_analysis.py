import sys
import type_validation as tv
import numpy as np
from type_specs import rel_level_p, nat_int_p
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations
from datetime import datetime, timedelta
from floodsystem.plot import plot_water_levels, plot_water_levels_no_show
from floodsystem.analysis import polyfit
import matplotlib

_o_polyfit = polyfit


def _i_polyfit(dates, levels, p):
    tv.assert_type(dates, (list, datetime))
    tv.assert_type(levels, (list, rel_level_p))
    tv.assert_type(p, nat_int_p)
    ret = _o_polyfit(dates, levels, p)
    tv.assert_type(ret, (tuple, [np.poly1d, timedelta]))
    return ret


polyfit = _i_polyfit

sample_dates = [datetime(2016, 12, 30), datetime(2016, 12, 31), datetime(2017, 1, 1),
                datetime(2017, 1, 2), datetime(2017, 1, 3), datetime(2017, 1, 4),
                datetime(2017, 1, 5)]
sample_levels = [0.2, 0.7, 0.95, 0.92, 1.02, 0.91, 0.64]

sample_dates2 = matplotlib.dates.num2date(np.linspace(10000, 10002, 10))
sample_levels2 = [0.1, 0.09, 0.23, 0.34, 0.78, 0.74, 0.43, 0.31, 0.01, -0.05]


def test_polyfit():
    # no errors should be thrown
    polyfit(sample_dates, sample_levels, 1)
    polyfit(sample_dates2, sample_levels2, 2)
    polyfit(sample_dates2, sample_levels2, 3)
    polyfit(sample_dates, sample_levels, 4)
