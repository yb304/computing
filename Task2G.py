import sys
import math
import collections
import pickle
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
# from test_analysis import polyfit
from floodsystem.analysis import polyfit
# from test_flood import stations_level_over_threshold
from floodsystem.flood import stations_level_over_threshold
from datetime import timedelta
from matplotlib.dates import date2num
import copy

risky_rwl_tol = 0.5
# number of days ahead to forecast water level
dt = 1
# number of days of water level history to use for the forecast
history_days = 4
# degree of polynomial to use for the forecast
poly_degree = 4
# multiplier used to discount forecasted risk levels
future_risk_weight = math.exp(-dt / 4)

rating_tol_severe = 3 - risky_rwl_tol
rating_tol_high = 2 - risky_rwl_tol
rating_tol_moderate = 1 - risky_rwl_tol


def stations_by_town(stations):
    ret = {}
    for s in stations:
        town = s.town
        if town in ret:
            ret[town].append(s)
        elif town is not None:
            ret[town] = [s]
    return ret


# to be populated by network request
measure_levels_by_station_id = None
measure_levels_save_file = "2G-measure-levels.pickle"


def get_measure_levels(station):
    global measure_levels_by_station_id
    if station.station_id in measure_levels_by_station_id:
        return measure_levels_by_station_id[station.station_id]
    else:
        print(
            f"Fetching water level history for: {station.name} ({station.station_id})"
        )
        ml = ([], [])
        try:
            ml = fetch_measure_levels(station.measure_id,
                                      timedelta(days=history_days))
        except Exception:
            print("WARNING: Failed to get water level history")
        measure_levels_by_station_id[station.station_id] = ml
        return ml


def save_measure_levels():
    global measure_levels_by_station_id
    with open(measure_levels_save_file, "wb") as f:
        pickle.dump(measure_levels_by_station_id, f)


def load_measure_levels():
    with open(measure_levels_save_file, "rb") as f:
        return pickle.load(f)


def to_forecasted_station(station, dt):
    """
    Modifies the state of the station to reflect the forecast
    `dt` days from the current point in time.
    [Imperative]
    """
    dates, levels = get_measure_levels(station)
    if len(dates) > 0:
        try:
            poly, offset = polyfit(dates, levels, poly_degree)
            dpoly = poly.deriv()
            dwldt = dpoly(date2num(max(dates) - offset))
            dwl = dwldt * dt
            station.latest_level += dwl
        except Exception:
            print(
                f"WARNING: Failed to compute forecast for station {station.name}. Data may be malformed."
            )


class Town:

    def __init__(self, name, stations):
        assert name is not None
        self.name = name
        self.stations = stations
        self.cached_risk_value = None

    def __repr__(self):
        return f"#Town['{self.name}' {list(map(lambda s: s.name, self.stations))}]"

    def instantaneous_risk_value(self):
        """Returns a value for the flood risk without considering the future or past"""
        # Low or negative relative water levels should not reduce overall risk
        risky_station_levels = stations_level_over_threshold(
            self.stations, risky_rwl_tol)
        rwl_sum = sum(map(lambda t: t[1] - risky_rwl_tol,
                          risky_station_levels))
        n = len(risky_station_levels)
        rwl_mean = rwl_sum / n if n > 0 else 0
        return rwl_mean

    def risk_value(self):
        """ Returns a number representing the flood risk. Minimum is 0 (no risk) """
        if self.cached_risk_value is None:
            risk1 = self.instantaneous_risk_value()

            # Forecast water level into the future
            # Inflate the risk if it is increasing
            future_town = copy.deepcopy(self)
            for station in future_town.stations:
                to_forecasted_station(station, dt)

            risk2 = future_town.instantaneous_risk_value()

            overall_risk = max(risk1, risk2 * future_risk_weight)
            self.cached_risk_value = overall_risk

        return self.cached_risk_value

    def risk_rating(self):
        risk = self.risk_value()
        if risk > rating_tol_severe:
            return "severe"
        elif risk > rating_tol_high:
            return "high"
        elif risk > rating_tol_moderate:
            return "moderate"
        else:
            return "low"


def towns_with_greatest_risk(towns, n):
    towns = filter(lambda t: t.risk_value() is not None, towns)
    return sorted(towns, key=lambda t: t.risk_value(), reverse=True)[:n]


def get_towns(stations):
    sbt = stations_by_town(stations)
    towns = map(lambda item: Town(item[0], item[1]), sbt.items())
    towns = list(towns)
    return towns


def present_towns_with_greatest_risk(towns, n):
    towns = towns_with_greatest_risk(towns, n)
    for i, town in enumerate(towns):
        risk = town.risk_value()
        assert risk is not None
        rating = town.risk_rating()
        print(f"{i+1:3}) {risk:6.2f} {town.name:40} ({rating})")


def ask_for_n():
    n = None
    while n is None:
        nin = input("How many towns do you want to list? ")
        try:
            n = int(nin)
            if n < 0:
                n = None
        except Exception:
            None
        if n is None:
            print("Wrong answer")
    return n


stations = build_station_list()
update_water_levels(stations)
all_towns = get_towns(stations)


def run():
    argn = int(sys.argv[1]) if len(sys.argv) > 1 else None

    global measure_levels_by_station_id
    try:
        measure_levels_by_station_id = load_measure_levels()
    except Exception:
        measure_levels_by_station_id = {}
        print("Warning: failed to load water level data from cache file")

    frequencies = dict(
        collections.Counter(map(lambda t: t.risk_rating(), all_towns)))
    print(f"\nOverall frequencies of risk ratings: {frequencies}")

    save_measure_levels()

    print("\nTowns where we assess the risk of flooding to be greatest.\n")
    n = ask_for_n() if argn is None else argn
    present_towns_with_greatest_risk(all_towns, n)


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()

exit()
# #### REPL #####

x = list(filter(lambda t: t.risk_value() > 0, all_towns))
risks = list(map(lambda t: t.risk_value(), x))
risks = sorted(risks)

fd = list(filter(lambda s: s.town == "Letcombe Bassett", stations))
ft = get_towns(fd)

ft[0].cached_risk_value = None
ft[0].risk_value()

present_towns_with_greatest_risk(x, 300)

measure_levels_by_station_id = load_measure_levels()
save_measure_levels()
