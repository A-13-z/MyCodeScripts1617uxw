import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Generate sample data
np.random.seed(0)
x = np.random.randn(1000)  # 1000 random points from a normal distribution
y = np.random.randn(1000)  # 1000 random points from a normal distribution

# Create a 2D histogram
plt.figure(figsize=(8, 6))
plt.hist2d(x, y, bins=30, density=True, cmap='viridis', alpha=0.5)

# Create a grid for KDE
xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()
xi = np.linspace(xmin, xmax, 100)
yi = np.linspace(ymin, ymax, 100)
xi, yi = np.meshgrid(xi, yi)

# Perform KDE
kde = gaussian_kde([x, y])
zi = kde(np.vstack([xi.flatten(), yi.flatten()]))
zi = zi.reshape(xi.shape)

# Plot the density heatmap
plt.contourf(xi, yi, zi, levels=30, cmap='viridis', alpha=0.7)

# Add a color bar
plt.colorbar(label='Density')

# Set labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Density Heatmap')

# Show plot
plt.show()
