import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Sample data
data = np.array([[8, 4, 3, 2, 3, 7, 5, 3, 7, 1, 10, 6, 1, 3, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3]])

# Generate heatmap
ax = sns.heatmap(data, cmap="YlGnBu")  # Using a specific colormap

cmap = plt.get_cmap('YlGnBu')

# Normalize data to the range [0, 1]
norm = plt.Normalize(vmin=data.min(), vmax=data.max())

# Get color for each value in the data
colors = cmap(norm(data))

print(colors*255)
