import floodsystem.geo as geo
import floodsystem.stationdata as sd


def demo_stations_by_river():
    stations = sd.build_station_list()
    sbr = geo.stations_by_river(stations)
    print("Stations by river:\n")
    for river in ["River Aire", "River Cam", "River Thames"]:
        names = sorted(map(lambda stn: stn.name, sbr[river]))
        print(f"  {river}:")
        print(f"    {names}\n")


if __name__ == "__main__":
    print("\n*** Task 1D: CUED Part IA Flood Warning System ***\n")
    demo_stations_by_river()
