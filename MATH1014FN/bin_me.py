import numpy as np

# Define the bin counts
bin_counts = np.array([0, 2, 12, 9, 25, 40, 24, 48, 44, 59, 68, 70, 94, 81, 107, 96, 120, 84, 71, 63, 49])

# Compute the cumulative sum of the bin counts
cumulative_freq = np.cumsum(bin_counts)

# Print the cumulative frequency
print(cumulative_freq)

scores = np.arange(0, 105, 5)

print(scores)

scores_interpolate = np.arange(0, 101)

#interp_results = np.interp(scores_interpolate, scores, cumulative_freq)

from scipy.interpolate import interp1d

# Create a cubic spline interpolation function
f = interp1d(scores, cumulative_freq, kind='cubic')

# Evaluate the function at the desired points
interp_results = f(scores_interpolate)

print(interp_results)

interp_results_percentage = 1 - (interp_results / np.max(interp_results))

print(interp_results_percentage)

print(interp_results_percentage[80])

import json

with open('MATH1014FN_results_percentage_cubic.json', 'w') as f:
    json.dump(list(interp_results_percentage), f)

interp_results = np.interp(scores_interpolate, scores, cumulative_freq)

print(interp_results)

interp_results_percentage = 1 - (interp_results / np.max(interp_results))

print(interp_results_percentage)

print(interp_results_percentage[80])

import json

with open('MATH1014FN_results_percentage.json', 'w') as f:
    json.dump(list(interp_results_percentage), f)