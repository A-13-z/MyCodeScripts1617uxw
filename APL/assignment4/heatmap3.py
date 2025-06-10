#Z = np.array([[8, 4, 3, 2, 3, 7, 5, 3, 7, 1, 10, 6, 1, 3, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3]*26])
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Example 1D array of integers
data = np.array([8, 4, 3, 2, 3, 7, 5, 3, 7, 1, 10, 6, 1, 3, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3])

# Find the maximum value
max_value = np.max(data)

# Compute the distance of each value from the maximum
distance_from_max = np.abs(data - max_value)

# Normalize the distance (0 at max value, larger distances get higher values)
normalized_distance = distance_from_max / np.max(distance_from_max)

# Define the grid size for the heatmap (odd to center at [0, 0])
grid_size = 27  # Must be an odd number for symmetry around center
center = grid_size // 2

# Create an empty grid for the heatmap
heatmap_data = np.zeros((grid_size, grid_size))

# Generate concentric circle distances
for i in range(grid_size):
    for j in range(grid_size):
        # Calculate Euclidean distance from the center
        dist = np.sqrt((i - center)**2 + (j - center)**2)
        # Assign distance as the value (normalized)
        heatmap_data[i, j] = dist

# Normalize the entire heatmap to range [0, 1]
heatmap_data = (heatmap_data - np.min(heatmap_data)) / (np.max(heatmap_data) - np.min(heatmap_data))

# Invert the colors so that the center (minimum distance) is darkest
#heatmap_data = 1 - heatmap_data
print(heatmap_data)
# Create the heatmap using Seaborn
plt.figure(figsize=(6, 6))
sns.heatmap(heatmap_data, cmap='plasma', cbar=True, square=True, linewidths=0)

# Add title and display the plot
plt.title('Radial Heatmap with Concentric Circles')
plt.axis('off')  # Turn off the axis for a cleaner look
plt.show()

cmap = plt.get_cmap('YlGnBu')

norm = plt.Normalize(vmin=data.min(), vmax=data.max())

colors = cmap(norm(data))

print(colors.shape)