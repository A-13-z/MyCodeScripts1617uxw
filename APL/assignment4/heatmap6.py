import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def create_radial_gradient(colors, size=(1000, 1000), base_color = (1, 1, 1)):
    # Create a meshgrid for the circle
    x = np.linspace(-1, 1, size[0])
    y = np.linspace(-1, 1, size[1])
    X, Y = np.meshgrid(x, y)
    
    # Calculate the radial distance from the center
    radius = np.sqrt(X**2 + Y**2)
    
    # Create a mask for the circle
    mask = radius <= 1 # Only keep points inside the unit circle
    radius = np.clip(radius, 0, 1)  # Normalize radius to [0, 1]
    fade_radius = 0.8
    fade_width = 0.2
    # Create a LinearSegmentedColormap
    # Normalize the color stops for the first color to occupy the majority
    num_colors = len(colors)
    color_gradient = []
    majority_ratio = 0.5
    # For the first color (occupying majority)
    interp_colors_majority = np.linspace(colors[0], colors[1], int(256 * majority_ratio)) if num_colors > 1 else [colors[0]]*4
    #print(colors[1] == colors[0] if num_colors > 1 else 2)
    color_gradient.append(interp_colors_majority)
    # For the remaining colors
    for i in range(1, num_colors - 1):
        c1 = np.concatenate((colors[i][:3], np.array(colors[i][3]*(1 - i/(num_colors - 1))).reshape(1)), axis = 0)
        c2 = np.concatenate((colors[i + 1][:3], np.array(colors[i + 1][3]*(1 - i/(num_colors - 1))).reshape(1)), axis = 0)
        c1 = colors[i]
        c2 = colors[i+1]
        interp_colors = np.linspace(c1, c2, int(256 * (1 - majority_ratio) / (num_colors - 1)))
        color_gradient.append(interp_colors)

    # Concatenate all the interpolated colors
    color_list = np.concatenate(color_gradient)
    
    # Create a colormap
    cmap = LinearSegmentedColormap.from_list("smooth_radial_gradient", color_list)

    # Map the normalized radius to the colormap
    gradient = cmap(radius)
    #gradient[radius > fade_radius] = gradient[radius > fade_radius]*(1-(radius[radius > fade_radius] - fade_radius)/fade_width)
    #gradient[~mask] = list(base_color) + [0]
    #gradient[~mask] = [for i in gradient[~mask]]
    l = len(gradient[~mask])
    # arr = gradient[~mask]
    # dummy = np.array([arr[i][:4] + [np.exp(-i/l)] for i in range(l)])
    # gradient[~mask] = dummy
    gradient[~mask] = [1, 1, 1, 0]
    return gradient
    # Display the gradient
    # plt.imshow(gradient, extent=(-1, 1, -1, 1), origin='lower')
    # plt.axis('off')
    # plt.show()
# Define the colors (in RGB format)
colors = [
    [1.0, 0.0, 0.0],  # c1: Red
    [0.0, 1.0, 0.0],  # c2: Green
    [0.0, 0.0, 1.0],  # c3: Blue
    [1.0, 1.0, 0.0],  # c4: Yellow
    [1.0, 0.0, 1.0],  # c5: Magenta
]
colors = np.array([
    [0.81662438, 0.92802768, 0.70302191, 1.        ],
 [0.93799308, 0.9758862,  0.71318724, 1.        ],
 [1.    ,     1.,       0.85098039, 1.        ],
 [1.   ,      1. ,        0.85098039, 1.        ],
 [1.  ,       1.  ,       0.85098039 ,1.        ],
 [1. ,        1.   ,      0.85098039, 1.        ],
 [1.,         1.,         0.85098039, 1.        ]])
 #[0.81662438, 0.92802768, 0.70302191, 1.        ]])
# Create and display the radial gradient
create_radial_gradient(colors)
