import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from .station import MonitoringStation
from .flood import stations_highest_rel_level



def plot_water_levels(station, dates, levels):
   
    # Plot
    plt.plot(dates, levels)

    # Add axis labels, rotate date labels and add plot title
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45);
    plt.title("Station A")

    # Display plot
    plt.tight_layout()  # This makes sure plot does not cut off date labels

    plt.show()
    return True

