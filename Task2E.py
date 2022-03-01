from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.plot import plot_water_levels
from datetime import timedelta

def run():

    stations = build_station_list()
    update_water_levels(stations)

    highest_5 = stations_highest_rel_level(stations, 5)
    dates = []
    levels = []
    for station in highest_5:
        date, level = fetch_measure_levels(station.measure_id, timedelta(10))
        dates.append(date)
        levels.append(level)

    plot_water_levels(highest_5, dates, levels)


if __name__ == "__main__":
    print("*** Task 2E: CUED Part IA Flood Warning System ***")
    run()