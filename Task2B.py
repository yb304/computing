from floodsystem.flood import stations_level_over_threshold
from floodsystem.stationdata import build_station_list, update_water_levels

def run():

    stations = build_station_list()
    update_water_levels(stations)

    for n in stations_level_over_threshold(stations, 0.9):
        print("Station name and current level: {}, {}".format(
            n[0].name), n[1].relative_water_level)

if __name__ == "__main__":
    print("*** Task 2B: CUED Part IA Flood Warning System ***")
    run()
