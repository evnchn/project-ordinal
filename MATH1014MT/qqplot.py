import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Define the frequency of the bins
freq = [0, 22, 61, 132, 151, 159, 201, 180, 163, 91, 32]

# Calculate the cumulative distribution function (CDF) of the data
cum_freq = np.cumsum(freq)
cum_freq_norm = cum_freq / cum_freq[-1]

# Generate a normal distribution with the same mean and standard deviation as the data
mu, sigma = stats.norm.fit(np.arange(0, 101, 10))
print(mu, sigma)
mu, sigma = 53, 21 # from email
norm_dist = stats.norm(mu, sigma)

# Calculate the theoretical quantiles of the normal distribution
theoretical_quantiles = norm_dist.ppf(cum_freq_norm)

# Plot the Q-Q plot
plt.plot(theoretical_quantiles, np.arange(0, 101, 10), 'o')
plt.plot(np.arange(0, 101, 10), np.arange(0, 101, 10), '-')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.title('Q-Q Plot')
plt.show()