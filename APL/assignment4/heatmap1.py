import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Define the size of the heatmap (e.g., 100x100)
size = 100

# Generate a coordinate grid
x = np.linspace(-1, 1, size)
y = np.linspace(-1, 1, size)
X, Y = np.meshgrid(x, y)

# Calculate the radial distance from the center
Z = np.sqrt(X**2 + Y**2)  # Distance from the origin

# Optionally, normalize Z to the range [0, 1]
Z_normalized = (Z - np.min(Z)) / (np.max(Z) - np.min(Z))

# Create the heatmap with Seaborn
plt.figure(figsize=(6, 6))  # Adjust figure size for square aspect
sns.heatmap(Z_normalized, cmap='coolwarm', cbar=True)

# Set title and show the plot
plt.title('Radial Gradient Heatmap')
plt.show()
