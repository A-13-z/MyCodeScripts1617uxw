import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from heatmap6 import create_radial_gradient
from qwerty_layout import keys

hash = {'Shift_L': 8, 'i': 4, 'w': 3, 'a': 2, 's': 3, 'l': 7, 'o': 5, 'n': 3, 'e': 7, 'y': 1, 't': 10, 'h': 6, 'd': 1, 'f': 3, 'c': 1, 'u': 3, 'v': 1, '2': 1, 'm': 1, 'r': 2, 'b': 1, '4': 1, 'g': 1, '8': 1, '.': 1, '1': 3}
data = np.array([list(hash.values())])

ax = sns.heatmap(data, cmap="viridis")

cmap = plt.get_cmap('viridis')

norm = plt.Normalize(vmin=data.min(), vmax=data.max())

colors = cmap(norm(data))

colors = colors.reshape(len(hash), 4)
#print(colors)
dct = {i:j for i, j in zip(list(hash.keys()), colors)}

new_dct = {}

sorted_values = sorted(list(hash.values()))
sorted_dict = dict(sorted(hash.items(), key=lambda item: item[1]))
base_color = None
for i in sorted_values:
    temp = []
    for key, value in sorted_dict.items():
        if value <= i:
            temp += [dct[key]]*value
        if value == i:
            base_color = temp[0]
            new_dct[key.lower()] = temp[::-1]

# for i0 in sorted_values:
#     new_dct[i0] = [dct[i] for i in sorted_values if hash.key <= hash[i0]][::-1]

# Print or use new_dct
#print(new_dct['t'])

# keys = [
#     ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
#     ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
#     ['Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
#     ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
#     ['Ctrl', 'Alt', 'Space', 'Alt', 'Ctrl']
# ]

# sizes = [
#     [1] * 13 + [2], # Row 1 (Backspace is larger)
#     [1.5] + [1] * 12 + [1.5], # Row 2 (Tab, and backslash)
#     [1.75] + [1] * 11 + [2.25], # Row 3 (Caps and Enter)
#     [2.25] + [1] * 10 + [2.25], # Row 4 (Shift keys)
#     [1.5, 1.5, 6, 1.5, 1.5] # Row 5 (Space bar and modifiers)
# ]

fig, ax = plt.subplots(figsize=(14, 6))

x, y = 0, 0  # Starting position for keys
key_height = 0.7  # Height of each key
spacing = 0.1  # Space between keys
key_width = 0.7
# Iterate over rows of keys
# for row, row_sizes in zip(keys, sizes):
#     x = 0
#print(dct.keys())
for key in list(keys.keys()):
    x, y = keys[key]['pos']
    #print(key.lower())
    if key in dct.keys():
        gradient = create_radial_gradient(new_dct[key.lower()], base_color = base_color)
        ax.add_patch(plt.Rectangle((x - key_width/2, y - key_height/2), key_width, key_height, edgecolor='black', facecolor=base_color, alpha = 0))
        ax.imshow(gradient, extent=(x - key_width/2 - 0.1, x + key_width/2 + 0.1, y - key_height/2 - 0.1, y + key_height/2 + 0.1))
        
    else:
        ax.add_patch(plt.Rectangle((x - key_width/2, y - key_height/2), key_width, key_height, edgecolor='black', facecolor='lightgray'))

    ax.text(x, y, key, ha='center', va='center', fontsize=10, color = 'orange')
        
        #x += key_width + spacing

    #y -= key_height + spacing

ax.set_xlim(-1, 14)
ax.set_ylim(-1, 5)

ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.show()
