import pprint as pp
import floodsystem.geo as geo
import floodsystem.stationdata as sd


stations = sd.build_station_list()

cam_centre_pos = (52.2053, 0.1218)


if __name__ == "__main__":
    print("\n*** Task 1B: CUED Part IA Flood Warning System ***\n")
    stations_by_dist = \
        list(map(lambda r:
                 (r[0].name, r[0].town, r[1]),
                 geo.stations_by_distance(stations, cam_centre_pos)))
    print("10 Closest stations:")
    pp.pprint(stations_by_dist[:10])
    print("\n10 Farthest stations:")
    pp.pprint(stations_by_dist[-10:])
