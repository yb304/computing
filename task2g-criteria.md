# Criteria Used for Determining Towns Most at Risk of Flooding

- Only stations with a relative water level (RWL) above 0.5 contribute to the risk.
  - This is to prevent stations with a very low or negative RWL from significantly reducing the risk rating when in reality a river with a very low water level does not compensate for another river that is flooding in the same town..
- For each town, the RWL of the considered stations are averaged to prevent the number of monitoring stations in the town from having a significant impact on the risk rating (it would not make sense to simply add up the RWLs of each).
- The average RWL value is reduced by 0.5 to provide continuity such that the risk number scales continuously from 0. This results in the instantaneous risk value.
- The above procedure is repeated for the forecasted water levels of each station one day into the future.
- The future water levels is determined by calculating the best-fit polynomial of degree 4 on the water level history of each station over the last four days. Data beyond four days was not included as this would increase the size of the dataset, and it is already very slow fetching all of the water level histories over the network for each station sequentially.
  - From the polynomial, the gradient (derivative) is calculated at the latest point which is then used to linearly extrapolate the water level line one day into the future.
- The future risk value is reduced by multiplying it by a 'weight'. This is because the future predictions should not be as influencial as the present data because of the uncertainty as well as the fact that events further out into the future tend to be less relevant and important.
- To determine the final value for risk, the maximum of the present risk value and weighted future risk value is taken. The maximum was used because a low risk in the near future does not compensate for record-breaking flooding in the present, for example; an extreme of either the present or future risk cannot be ignored.
