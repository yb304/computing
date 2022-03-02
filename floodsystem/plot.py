import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from .station import MonitoringStation
from .flood import stations_highest_rel_level


def plot_water_levels_no_show(station, dates, levels):
    plt.plot(dates, levels, label="Actual")

    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)

    # Plot max and min typical water level
    if len(dates) > 0:
        plt.axhline(station.typical_range[1],
                    linestyle="dashed",
                    color="red",
                    label="Typical high level")
        plt.axhline(station.typical_range[0],
                    linestyle="dashed",
                    color="orange",
                    label="Typical low level")

    plt.legend()
    # Prevent date labels being cut off
    plt.tight_layout()


def plot_water_levels(station, dates, levels):
    plot_water_levels_no_show(station, dates, levels)
    plt.show()
