import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from .station import MonitoringStation
from .flood import stations_highest_rel_level

t = [datetime(2022, 2, 19), datetime(2022, 2, 20), 
    datetime(2022, 2, 21), datetime(2022, 2, 22), datetime[2022, 2, 23],
    datetime[2022, 2, 24], datetime[2022, 2, 25], datetime[2022, 2, 26],
    datetime[2022, 2, 27], datetime[2022, 2, 28]]

def plot_water_levels(station, dates, levels):
   
    # Plot
    plt.plot(t, levels)

    # Add axis labels, rotate date labels and add plot title
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45);
    plt.title("Station A")

    # Display plot
    plt.tight_layout()  # This makes sure plot does not cut off date labels

    plt.show()
    return True

