### standard imports
import matplotlib.pyplot as plt
import numpy as np
import random

#qwerty_layout from which keys and characters are imported (additional file)
from qwerty_layout import keys, characters

#for comparison purposes
#random.seed(42)

def optimization(text):
    def calculate_total_distance(text, keys = keys, characters = characters):
            distance_map = {}
            for i in text:
                if i in characters.keys():
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

            return sum(distance_map.values())

    def optimize_layout(text, keys, characters, iterations=1000, temperature=1000, cooling_rate=0.9):
        #only need to find the positions of the keys - no need for characters dictionary to be modified
        current_layout = keys.copy()
        #calculate the current distance
        current_distance = calculate_total_distance(text, current_layout, characters)
        
        #initialize best layout as the current layout
        best_layout = current_layout.copy()
        #initialize the best distance as the current distance
        best_distance = current_distance
        
        #distances over all iterations
        distances = [current_distance]  
        
        for _ in range(iterations):
            #pick two random keys to swap
            key1, key2 = random.sample(list(current_layout.keys()), 2)
            
            #swap their positions along with where the distance is measured from
            if key2 != current_layout[key2]['start'] and key1 != current_layout[key1]['start']:
                current_layout[key1], current_layout[key2] = current_layout[key2], current_layout[key1]
            elif key1 == current_layout[key1]['start']:
                for k in current_layout.keys():
                    if current_layout[k]['start'] == key1:
                        current_layout[k]['start'] = key2
                current_layout[key1], current_layout[key2] = current_layout[key2], current_layout[key1]
            elif key2 == current_layout[key2]['start']:
                for k in current_layout.keys():
                    if current_layout[k]['start'] == key2:
                        current_layout[k]['start'] = key1
                current_layout[key1], current_layout[key2] = current_layout[key2], current_layout[key1]
            
            #calculate the distance after swap
            new_distance = calculate_total_distance(text, current_layout, characters)
            
            #if the new distance is better, accept the swap - greedy approach
            if new_distance < current_distance:
                current_distance = new_distance
                if new_distance < best_distance:
                    best_layout = current_layout.copy()
                    best_distance = new_distance
            else:
                #accept worse solutions with some probability - exploration
                prob_accept = np.exp((current_distance - new_distance) / temperature)
                if random.random() < prob_accept:
                    current_distance = new_distance
                else:
                    #undo the swap
                    if key2 != current_layout[key2]['start'] and key1 != current_layout[key1]['start']:
                        current_layout[key1], current_layout[key2] = current_layout[key2], current_layout[key1]
                    elif key1 == current_layout[key1]['start']:
                        for k in current_layout.keys():
                            if current_layout[k]['start'] == key1:
                                current_layout[k]['start'] = key2
                        current_layout[key1], current_layout[key2] = current_layout[key2], current_layout[key1]
                    elif key2 == current_layout[key2]['start']:
                        for k in current_layout.keys():
                            if current_layout[k]['start'] == key2:
                                current_layout[k]['start'] = key1
                        current_layout[key1], current_layout[key2] = current_layout[key2], current_layout[key1]
            
            #update temperature and store the distance
            temperature *= cooling_rate
            distances.append(current_distance)
        
        return best_layout, distances

    best_layout, distances = optimize_layout(text, keys, characters)

    #plot the costs (distance) over all iterations
    def plot_cost_reduction(costs):
        plt.plot(costs)
        plt.xlabel('Iterations')
        plt.ylabel('Total Distance')
        plt.title('Cost Reduction During Optimization')
        plt.show()

    def visualise_keyboard(keys):
        fig, ax = plt.subplots(figsize=(14, 6))
        x, y = 0, 0
        key_height = 0.7
        key_width = 0.7

        #plot the keyboard layout (taking all keys to be square)
        for key in list(keys.keys()):
            x, y = keys[key]['pos']
            ax.add_patch(plt.Rectangle((x - key_width / 2, y - key_height / 2), key_width, key_height, edgecolor='black', facecolor='lightgray'))

            ax.text(x, y, key.title(), ha='center', va='center', fontsize=10, color='black')

        #set axis limits, aspect ratio, and hide the axes
        ax.set_xlim(-1, 14)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout()
        plt.show()

    #total distance cost vs iterations
    plot_cost_reduction(distances)
    #keyboard layout
    visualise_keyboard(best_layout)

#function call
optimization(text = '''Hey! how have you been?
             I have been well.''')