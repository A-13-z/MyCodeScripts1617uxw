import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

#assuming 'qwerty_layout' has 'keys' and 'characters' dictionaries.
#import qwerty_layout
### if using a module then pass module.keys and module.characters

#function to calculate distances and character frequencies
def heatmap(text, keys, characters):
    def distance_calculation(text, keys, characters):
        freq_map = {}   #keeps count of characters
        distance_map = {}   #keeps count of distance for each character
        
        #fill freq_map
        for i in text:
            for char in characters[i]:
                if char not in freq_map:
                    freq_map[char] = 1
                else:
                    freq_map[char] += 1

        #fill distance_map
        for i in text:
            for char in characters[i]:
                pos, start = keys[char]['pos'], keys[char]['start']
                posn_start = keys[start]['pos']
                x, y = pos
                x0, y0 = posn_start
                dist = ((x - x0)**2 + (y - y0)**2)**0.5
                if char not in distance_map:
                    distance_map[char] = dist
                else:
                    distance_map[char] += dist

        return freq_map, sum(distance_map.values())

    #create a radial gradient
    def create_radial_gradient(colors, size=(1000, 1000)):
        #taking as many points as possible for "resolution" or good transition
        x = np.linspace(-1, 1, size[0])
        y = np.linspace(-1, 1, size[1])
        X, Y = np.meshgrid(x, y)
        radius = np.sqrt(X**2 + Y**2)
        #get a circle
        mask = radius <= 1
        radius = np.clip(radius, 0, 1)
        
        num_colors = len(colors)
        color_gradient = []
        #majority would be the color corresponding to the frequency of that character
        majority_ratio = 0.5
        #smooth gradient for the majority color
        interp_colors_majority = np.linspace(colors[0], colors[1], int(256 * majority_ratio)) if num_colors > 1 else [colors[0]] * 4
        color_gradient.append(interp_colors_majority)
        
        #creating transition for the other colors
        for i in range(1, num_colors - 1):
            c1 = colors[i]
            c2 = colors[i + 1]
            interp_colors = np.linspace(c1, c2, int(256 * (1 - majority_ratio) / (num_colors - 1)))
            color_gradient.append(interp_colors)
        
        #joining the colors
        color_list = np.concatenate(color_gradient)
        cmap = LinearSegmentedColormap.from_list("smooth_radial_gradient", color_list)
        gradient = cmap(radius)
        #setting the background to white
        gradient[~mask] = [1, 1, 1, 0]
        return gradient

    #distance and data
    hash, distance = distance_calculation(text, keys, characters)

    #create the color mapping based on frequency values
    data = np.array([list(hash.values())])
    cmap = plt.get_cmap('magma')
    norm = plt.Normalize(vmin=data.min(), vmax=data.max())
    colors = cmap(norm(data))
    colors = colors.reshape(len(hash), 4)
    dct = {i: j for i, j in zip(list(hash.keys()), colors)}

    #to layer the heatmap circle/contours appropriately based on their relative frequency
    new_dct = {}
    sorted_values = sorted(list(hash.values()))
    sorted_dict = dict(sorted(hash.items(), key=lambda item: item[1]))

    for i in sorted_values:
        temp = []
        for key, value in sorted_dict.items():
            if value <= i:
                for _ in range(1, value + 1):
                    temp1 = np.concatenate((dct[key][:3], np.array([dct[key][3] * (value / max(sorted_values))])), axis=0)
                    if not any(np.array_equal(temp1, arr) for arr in temp):
                        temp.append(temp1)
            if value == i:
                new_dct[key.lower()] = temp[::-1]

    #create the figure and axes for the keyboard layout
    fig, ax = plt.subplots(figsize=(14, 6))
    x, y = 0, 0
    key_height = 0.7
    key_width = 0.7

    #plot the keyboard layout and generate gradients (and map them to corresponding key)
    for key in list(keys.keys()):
        x, y = keys[key]['pos']
        
        if key in dct.keys():
            gradient = create_radial_gradient(new_dct[key.lower()])
            if key.lower() == 'space':
                ax.add_patch(plt.Rectangle((x - 2 * key_width, y - key_height / 2), 4 * key_width, key_height, edgecolor='black', facecolor='lightgrey'))
                ax.imshow(gradient, extent=(x - key_width / 2, x + key_width / 2, y - key_height / 2, y + key_height / 2), zorder=1) 
            elif key.lower() == 'shift_l' or key.lower() == 'shift_r':
                ax.add_patch(plt.Rectangle((x - key_width / 2, y - key_height / 2), 2 * key_width, key_height, edgecolor='black', facecolor='lightgray'))
                ax.imshow(gradient, extent=(x - key_width / 2, x + key_width / 2, y - key_height / 2, y + key_height / 2), zorder=1) 
            else:
                ax.add_patch(plt.Rectangle((x - key_width / 2, y - key_height / 2), key_width, key_height, edgecolor='black', facecolor='lightgray'))
                ax.imshow(gradient, extent=(x - key_width / 2, x + key_width / 2, y - key_height / 2, y + key_height / 2), zorder=1)         
        else:
            if key.lower() == 'space':
                ax.add_patch(plt.Rectangle((x - 2 * key_width, y - key_height / 2), 4 * key_width, key_height, edgecolor='black', facecolor='lightgrey'))
            elif key.lower() == 'shift_l' or key.lower() == 'shift_r':
                ax.add_patch(plt.Rectangle((x - key_width / 2, y - key_height / 2), 2 * key_width, key_height, edgecolor='black', facecolor='lightgray'))
            else:
                ax.add_patch(plt.Rectangle((x - key_width / 2, y - key_height / 2), key_width, key_height, edgecolor='black', facecolor='lightgray'))

        ax.text(x, y, key.title(), ha='center', va='center', fontsize=10, color='black')

    #set axis limits, aspect ratio, and hide the axes
    ax.set_xlim(-1, 14)
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    #create a colorbar for the plot
    norm = plt.Normalize(vmin=min(sorted_values), vmax=max(sorted_values))
    cbar = plt.cm.ScalarMappable(cmap='magma', norm=norm)
    cbar.set_array([])
    fig.colorbar(cbar, ax=ax, orientation='horizontal').set_label('Frequency of Characters')

    plt.tight_layout()
    plt.show()
    print(f"Distance travelled: {distance:.3f}", f"for {text}")

#comment out to see execution
# heatmap("Lorem Ipsum Dolor Sit Amet.", qwerty_layout.keys, qwerty_layout.characters)
# heatmap("Hello World!!", qwerty_layout.keys, qwerty_layout.characters)