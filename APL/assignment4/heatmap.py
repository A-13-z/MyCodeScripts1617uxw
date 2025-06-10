import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

n = 1000  # Resolution of the gradient
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
X, Y = np.meshgrid(x, y)
Z = np.sqrt(X**2 + Y**2)

Z = Z / np.max(Z)

# Create a circular mask
radius = 0.1  # Radius of the circle
mask = Z <= radius  # True for points within the circle

# Apply the mask by setting outside values to NaN
gradient_circle = np.zeros(Z.shape)  # Start with a zero array
gradient_circle[mask] = Z[mask]  
gradient_circle[~mask] = np.nan
#artist = mpatches.Circle((0, 0), radius = 0.12, alpha = 0.5, facecolor = 'none')
artist1 = mpatches.Circle((0, 0), radius = 0.1, alpha = 0.8, facecolor = 'none')

ax = plt.gca()
ax.imshow(gradient_circle, extent=(-1, 1, -1, 1), origin='lower', cmap='viridis')
#ax.add_patch(artist)
ax.add_patch(artist1)
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

ax.set_aspect('equal', adjustable='box')
plt.show()