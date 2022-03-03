import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
from datetime import datetime, timedelta
from .station import MonitoringStation
from .flood import stations_highest_rel_level
from .analysis import polyfit


def plot_water_levels_no_show(station, dates, levels):
    plt.plot(dates, levels, label="Actual")

    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)

    # Plot max and min typical water level
    if len(dates) > 0:
        plt.axhline(station.typical_range[1],
                    linestyle="dashed",
                    color="red",
                    label="Typical high level",
                    marker="None")
        plt.axhline(station.typical_range[0],
                    linestyle="dashed",
                    color="orange",
                    label="Typical low level",
                    marker="None")

    plt.legend()
    # Prevent date labels being cut off
    plt.tight_layout()


def plot_water_levels(station, dates, levels):
    """
    Displays a Matplotlib plot of the provided water level data against time for a station.
    The typical low and high levels are also plotted.

    Args:
      station: MonitoringStation object
      dates: list of datetime objects
      levels: list of water levels (floats)
    """
    plot_water_levels_no_show(station, dates, levels)
    plt.show()


def systematic_sample(coll, interval):
    # always collects the first item
    reduced = []
    i = interval
    for x in coll:
        if i == interval:
            i = 0
            reduced.append(x)
        i += 1

    return reduced


def plot_water_level_with_fit(station, dates, levels, p):
    """
    Plots the water level history for a station
    superposed with the best-fit polynomial.
    Note: does not show the plot.
    Args:
      station: MonitoringStation object
      dates: list of datetime objects (x axis)
      levels: list of water levels (y axis)
    """
    plt.rc("lines", marker=".", linestyle="None")
    plot_water_levels_no_show(station, dates, levels)
    matplotlib.pyplot.rcdefaults()
    poly, offset = polyfit(dates, levels, p)

    nsamples = 42
    interval = math.ceil((len(dates) - 1) / nsamples)
    dates_reduced = systematic_sample(dates[:-1], interval)
    dates_reduced.append(dates[-1])
    xs = np.array(
        list(
            map(lambda d: matplotlib.dates.date2num(d - offset),
                dates_reduced)))
    plt.plot(dates_reduced,
             poly(xs),
             label=f"Best-fit polynomial of degree {p}",
             color="green")
    plt.legend()
