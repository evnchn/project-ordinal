import json

import numpy as np
from scipy.interpolate import interp1d

# Define the bin counts
bin_counts = np.array([0, 22, 61, 132, 151, 159, 201, 180, 163, 91, 32])

# Compute the cumulative sum of the bin counts
cumulative_freq = np.cumsum(bin_counts)

# Print the cumulative frequency
print(cumulative_freq)

scores = np.arange(0, 110, 10)

print(scores)

scores_interpolate = np.arange(0, 101)

#interp_results = np.interp(scores_interpolate, scores, cumulative_freq)

# Create a cubic spline interpolation function
f = interp1d(scores, cumulative_freq, kind='cubic')

# Evaluate the function at the desired points
interp_results = f(scores_interpolate)

print(interp_results)

interp_results_percentage = 1 - (interp_results / np.max(interp_results))

print(interp_results_percentage)

print(interp_results_percentage[80])

with open('MATH1014MT_results_percentage_cubic.json', 'w') as f:
    json.dump(list(interp_results_percentage), f)

interp_results = np.interp(scores_interpolate, scores, cumulative_freq)

print(interp_results)

interp_results_percentage = 1 - (interp_results / np.max(interp_results))

print(interp_results_percentage)

print(interp_results_percentage[80])

with open('MATH1014MT_results_percentage.json', 'w') as f:
    json.dump(list(interp_results_percentage), f)
