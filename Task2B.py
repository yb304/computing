from floodsystem.flood import stations_level_over_threshold
from floodsystem.stationdata import build_station_list, update_water_levels


def run():
    stations = build_station_list()
    update_water_levels(stations)

    print("\nRelative water levels of stations where it is >0.8:\n")
    for station, rwl in stations_level_over_threshold(stations, 0.8):
        print(f"{station.name:<50} {rwl:11.6f}")


if __name__ == "__main__":
    print("*** Task 2B: CUED Part IA Flood Warning System ***")
    run()
