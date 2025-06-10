import matplotlib.pyplot as plt
import matplotlib

import matplotlib.pyplot as plt

# Define the QWERTY keyboard layout
keys = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
    ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
    ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
    ['Ctrl', 'Alt', 'Space', 'Alt', 'Ctrl']
]

# Key sizes for each row (number of units per key)
sizes = [
    [1] * 13 + [2], # Row 1 (Backspace is larger)
    [1.5] + [1] * 12 + [1.5], # Row 2 (Tab, and backslash)
    [1.75] + [1] * 11 + [2.25], # Row 3 (Caps and Enter)
    [2.25] + [1] * 10 + [2.25], # Row 4 (Shift keys)
    [1.5, 1.5, 6, 1.5, 1.5] # Row 5 (Space bar and modifiers)
]

# Increase figure size
fig, ax = plt.subplots(figsize=(14, 6))  # Increase width and height

x, y = 0, 0  # Starting position for keys
key_height = 0.7  # Height of each key
spacing = 0.1  # Space between keys

# Iterate over rows of keys
for row, row_sizes in zip(keys, sizes):
    x = 0  # Reset x for each row
    for key, key_width in zip(row, row_sizes):
        # Draw the rectangle for the key
        ax.add_patch(plt.Rectangle((x, y), key_width, key_height, edgecolor='black', facecolor='lightgray'))

        # Add the label of the key
        ax.text(x + key_width / 2, y + key_height / 2, key, ha='center', va='center', fontsize=10)
        
        # Update the x position for the next key
        x += key_width + spacing

    # Update the y position for the next row
    y -= key_height + spacing

# Adjust axis limits based on the final x, y values
ax.set_xlim(0, 16.32)
ax.set_ylim(y + key_height - spacing, 1)

# Set the aspect ratio and turn off axis display
ax.set_aspect('equal')
ax.axis('off')

# Show the plot
plt.tight_layout()
plt.show()
