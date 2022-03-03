# Provide a program that for each of the 5 stations at which the
# current relative water level is greatest and
# for a time period extending back 2 days
# plots the level data and the best-fit polynomial of degree 4 against time.
# Show the typical range low/high on your plot.

from datetime import timedelta
import matplotlib.pyplot as plt
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from test_flood import stations_highest_rel_level
from test_analysis import polyfit
from test_plot import plot_water_levels_no_show, plot_water_level_with_fit


def run():
    stations = build_station_list()
    update_water_levels(stations)

    highest_stns = stations_highest_rel_level(stations, 5)
    for i, s in enumerate(highest_stns):
        dates, levels = fetch_measure_levels(s.measure_id, timedelta(days=2))
        if len(dates) == 0:
            print(f"Warning: no level history data found for station:\n{s}")
            continue

        plt.figure(i + 1)
        plot_water_level_with_fit(s, dates, levels, 4)

    plt.show()


if __name__ == "__main__":
    print("*** Task 2F: CUED Part IA Flood Warning System ***")
    run()
