from floodsystem.stationdata import build_station_list
from floodsystem.station import inconsistent_typical_range_stations


def run():
    list_needed = inconsistent_typical_range_stations(build_station_list())
    print(sorted([n.name for n in list_needed]))


if __name__ == "__main__":
    print("*** Task 1F: CUED Part IA Flood Warning System ***")
    run()
