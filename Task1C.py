from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_within_radius

Cambridge_city_centre = (52.2053, 0.1218)


def run():
    stations = stations_within_radius(build_station_list(),
                                      Cambridge_city_centre, 10)
    print(sorted([x.name for x in stations]))


if __name__ == "__main__":
    print("*** Task 1C: CUED Part IA Flood Warning System ***")
    run()
