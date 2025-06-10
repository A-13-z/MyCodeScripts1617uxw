def distance_calculation(text, layout):
    keys = layout.keys
    characters = layout.characters
    freq_map = {}
    distance_map = {}
    for i in text:
        for char in characters[i]:
            if char not in freq_map.keys():
                freq_map[char] = 1
            else:
                freq_map[char] += 1
        
    for i in text:
        for char in characters[i]:
            pos, start = keys[char]['pos'], keys[char]['start']
            posn_start = keys[start]['pos']
            x, y = pos
            x0, y0 = posn_start
            dist = ((x - x0)**2 + (y - y0)**2)**0.5
            if char not in distance_map.keys():
                distance_map[char] = dist
            else:
                distance_map[char] += dist

        return freq_map, sum(distance_map.values())

import qwerty_layout
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

def create_radial_gradient(colors, size=(1000, 1000), base_color = (1, 1, 1)):
    #create a meshgrid for the circle
    x = np.linspace(-1, 1, size[0])
    y = np.linspace(-1, 1, size[1])
    X, Y = np.meshgrid(x, y)
    
    #calculate the radial distance from the center
    radius = np.sqrt(X**2 + Y**2)
    
    #create mask for the circle
    mask = radius <= 1 #keep points inside the unit circle
    radius = np.clip(radius, 0, 1)  #normalize radius to [0, 1]
    #create a LinearSegmentedColormap
    #normalize the color stops for the first color to occupy the majority
    num_colors = len(colors)
    color_gradient = []
    majority_ratio = 0.5
    #for the first color (majority color)
    interp_colors_majority = np.linspace(colors[0], colors[1], int(256 * majority_ratio)) if num_colors > 1 else [colors[0]]*4
    color_gradient.append(interp_colors_majority)
    #for the remaining colors
    for i in range(1, num_colors - 1):
        c1 = colors[i]
        c2 = colors[i+1]
        interp_colors = np.linspace(c1, c2, int(256 * (1 - majority_ratio) / (num_colors - 1)))
        color_gradient.append(interp_colors)

    #join all the interpolated colors
    color_list = np.concatenate(color_gradient)
    
    #create a colormap
    cmap = LinearSegmentedColormap.from_list("smooth_radial_gradient", color_list)

    #map the normalized radius to the colormap
    gradient = cmap(radius)
    #set white for all points outside the circle
    gradient[~mask] = [1, 1, 1, 0]
    #return gradient colors
    return gradient

keys = qwerty_layout.keys

hash, distance = distance_calculation("I have you.", qwerty_layout)
#hash = {'Shift_L': 8, 'i': 4, 'w': 3, 'a': 2, 's': 3, 'l': 7, 'o': 5, 'n': 3, 'e': 7, 'y': 1, 't': 10, 'h': 6, 'd': 1, 'f': 3, 'c': 1, 'u': 3, 'v': 1, '2': 1, 'm': 1, 'r': 2, 'b': 1, '4': 1, 'g': 1, '8': 1, '.': 1, '1': 3}
data = np.array([list(hash.values())])

ax = sns.heatmap(data, cmap="magma")
cbar = ax.get_children()[0]
plt.close()

cmap = plt.get_cmap('magma')

norm = plt.Normalize(vmin=data.min(), vmax=data.max())

colors = cmap(norm(data))

colors = colors.reshape(len(hash), 4)
#print(colors)
dct = {i:j for i, j in zip(list(hash.keys()), colors)}
#print(dct.values())
new_dct = {}

sorted_values = sorted(list(hash.values()))
sorted_dict = dict(sorted(hash.items(), key=lambda item: item[1]))
base_color = None
for i in sorted_values:
    temp = []
    for key, value in sorted_dict.items():
        if value <= i:
            for j in range(1, value + 1):
                #setting alpha according to the relative frequency
                temp1 = np.concatenate((dct[key][:3], np.array([dct[key][3]*(value/max(sorted_values))])), axis = 0)
                #ensuring unique value end up in the list
                if not any(np.array_equal(temp1, arr) for arr in temp):
                    temp.append(temp1)
        if value == i:
            base_color = temp[0]
            new_dct[key.lower()] = temp[::-1]

fig, ax = plt.subplots(figsize=(14, 6))

x, y = 0, 0  # Starting position for keys
key_height = 0.7  # Height of each key
spacing = 0.1  # Space between keys
key_width = 0.7
#print(new_dct)
for key in list(keys.keys()):
    x, y = keys[key]['pos']
    #print(key.lower())
    
    if key in dct.keys():
        gradient = create_radial_gradient(new_dct[key.lower()], base_color = base_color)
        if key.lower() == 'space':
            ax.add_patch(plt.Rectangle((x - 2*key_width, y - key_height/2), 4*key_width, key_height, edgecolor='black', facecolor='lightgrey'))
            ax.imshow(gradient, extent=(x - key_width/2, x + key_width/2, y - key_height/2, y + key_height/2), zorder = 1) 
        elif key.lower() == 'shift_l' or key.lower() == 'shift_r':
            ax.add_patch(plt.Rectangle((x - key_width/2, y - key_height/2), 2*key_width, key_height, edgecolor='black', facecolor='lightgray'))
            ax.imshow(gradient, extent=(x - key_width/2, x + key_width/2, y - key_height/2, y + key_height/2), zorder = 1) 
        else:
            ax.add_patch(plt.Rectangle((x - key_width/2, y - key_height/2), key_width, key_height, edgecolor='black', facecolor='lightgray'))
            ax.imshow(gradient, extent=(x - key_width/2, x + key_width/2, y - key_height/2, y + key_height/2), zorder = 1)         
    else:
        if key.lower() == 'space':
            ax.add_patch(plt.Rectangle((x - 2*key_width, y - key_height/2), 4*key_width, key_height, edgecolor='black', facecolor='lightgrey'))
        elif key.lower() == 'shift_l' or key.lower() == 'shift_r':
            ax.add_patch(plt.Rectangle((x - key_width/2, y - key_height/2), 2*key_width, key_height, edgecolor='black', facecolor='lightgray'))
        else:
            ax.add_patch(plt.Rectangle((x - key_width/2, y - key_height/2), key_width, key_height, edgecolor='black', facecolor='lightgray'))

    ax.text(x, y, key.title(), ha='center', va='center', fontsize=10, color = 'black')


ax.set_xlim(-1, 14)
ax.set_ylim(-1, 5)
fig.colorbar(cbar, ax=ax, orientation='horizontal').set_label('Frequency of Characters')
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.show()
