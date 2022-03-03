from datetime import timedelta
import numpy as np
import matplotlib


def polyfit(dates, levels, p):
    """
    Computes a least-squares fit for water level data of a station
    Args:
      dates: list of datetime objects (x axis)
      levels: list of water levels (y axis)
      p: degree of polynomial
    Returns:
      tuple of (polynomial object, shift of the time axis).
    """
    # as days since unix epoch
    date_floats = matplotlib.dates.date2num(dates)
    # Use time shift to avoid problems of floating point number round-off
    # being significant with high values of date_floats
    time_shift = date_floats[0]
    best_fit_coefficients = np.polyfit(date_floats - time_shift, levels, p)
    poly = np.poly1d(best_fit_coefficients)
    return poly, timedelta(days=time_shift)
