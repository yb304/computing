from test_flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels


def run():
    stations = build_station_list()
    update_water_levels(stations)

    n = 10
    print(
        f"\nRelative water levels of the {n} currently most at-risk stations:\n"
    )
    for station in stations_highest_rel_level(stations, n):
        print(f"{station.name:<50} {station.relative_water_level():11.6f}")


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
