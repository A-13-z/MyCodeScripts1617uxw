import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

X = np.linspace(-1, +1, 100)
Y = np.linspace(-1, 1, 100)
x, y = np.meshgrid(X, Y)
Z = np.exp(-(x**2 + y**2)*10)

ax = sns.heatmap(Z, cmap = 'coolwarm', cbar = False)
contour = plt.contourf(Z, levels = 10, cmap = 'coolwarm', alpha = 0.5)
#lines = plt.contour(data, levels = 10, colors = 'black', alpha = 0.5)
plt.show()