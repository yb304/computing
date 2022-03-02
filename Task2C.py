from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels


def run():

    stations = build_station_list()
    update_water_levels(stations)

    for station in stations_highest_rel_level(stations, 10):
        print("Station {} has current water level: {}".format(
            station.name, station.relative_water_level()))


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
