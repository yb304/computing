from datetime import timedelta
import matplotlib.pyplot as plt
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
from test_flood import stations_highest_rel_level
from test_analysis import polyfit
from test_plot import plot_water_levels_no_show, plot_water_level_with_fit


stations = build_station_list()
update_water_levels(stations)

town = input("Town: ")
filtered_stns = filter(lambda s: s.town == town, stations)
for i, s in enumerate(filtered_stns):
    dates, levels = fetch_measure_levels(s.measure_id, timedelta(days=4))
    print(s)
    print(f"relative level: {s.relative_water_level()}")
    if len(dates) == 0:
        print(f"Warning: no level history data found for station")
        continue

    plt.figure(i + 1)
    plot_water_level_with_fit(s, dates, levels, 4)

plt.show()
