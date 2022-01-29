import floodsystem.geo as geo
import floodsystem.stationdata as sd


stations = sd.build_station_list()


def demo_rivers_with_station():
    print("Rivers with station:\n")
    rivers = geo.rivers_with_station(stations)
    print(f"Number of rivers with at least one monitoring station: {len(rivers)}")
    print("First 10 rivers:")
    print(list(sorted(rivers))[:10])


def demo_stations_by_river():
    sbr = geo.stations_by_river(stations)
    print("Stations by river:\n")
    for river in ["River Aire", "River Cam", "River Thames"]:
        names = sorted(map(lambda stn: stn.name, sbr[river]))
        print(f"  {river}:")
        print(f"    {names}\n")


if __name__ == "__main__":
    print("\n*** Task 1D: CUED Part IA Flood Warning System ***\n")
    demo_rivers_with_station()
    print()
    demo_stations_by_river()
