import numpy as np

# Define the bin counts
bin_counts = np.array(
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3, 5, 3, 2, 13, 6.5, 1.5, 4.5, 4.5, 1.5, 1.5]
)
#                     [  0   5  10  15  20  25  30  35  40  45  50  55  60  65  70  75  80  85  90  95 100]

# Compute the cumulative sum of the bin counts
cumulative_freq = np.cumsum(bin_counts)

# Print the cumulative frequency
print(cumulative_freq)
print(len(cumulative_freq))

scores = np.arange(0, 105, 5)

print(scores)
print(len(scores))

scores_interpolate = np.arange(0, 100.1, 0.25)

# interp_results = np.interp(scores_interpolate, scores, cumulative_freq)

from scipy.interpolate import interp1d

# Create a cubic spline interpolation function
f = interp1d(scores, cumulative_freq, kind="cubic")

# Evaluate the function at the desired points
interp_results = f(scores_interpolate)

print(interp_results)

interp_results_percentage = 1 - (interp_results / np.max(interp_results))

print(interp_results_percentage)

print(interp_results_percentage[80])

import json

with open("COMP2012HMT_results_percentage_cubic.json", "w") as f:
    json.dump(list(interp_results_percentage), f)

interp_results = np.interp(scores_interpolate, scores, cumulative_freq)

print(interp_results)

interp_results_percentage = 1 - (interp_results / np.max(interp_results))

print(interp_results_percentage)

print(interp_results_percentage[80])

import json

with open("COMP2012HMT_results_percentage.json", "w") as f:
    json.dump(list(interp_results_percentage), f)
