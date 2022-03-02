from test_flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from test_plot import plot_water_levels
from datetime import timedelta


def run():

    stations = build_station_list()
    update_water_levels(stations)

    highest_5 = stations_highest_rel_level(stations, 5)

    for station in highest_5:
        dates, levels = fetch_measure_levels(station.measure_id, timedelta(days=10))
        plot_water_levels(station, dates, levels)


if __name__ == "__main__":
    print("*** Task 2E: CUED Part IA Flood Warning System ***")
    run()
