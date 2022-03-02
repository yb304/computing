from test_flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels


def run():
    stations = build_station_list()
    update_water_levels(stations)

    print("\nCurrent station relative water levels:")
    for station in stations_highest_rel_level(stations, 10):
        print(f"{station.name:<50} {station.relative_water_level():>10}")


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
