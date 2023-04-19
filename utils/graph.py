import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os


def graphing(chromosome, points, file_name = 'test'):
    selected = np.empty((len(np.where(chromosome == 1)[0]), 2))
    non_selected = np.empty((len(points) - len(np.where(chromosome == 1)[0]), 2)) 

    selected_i = 0
    non_selected_i = 0

    for i in range(0, len(chromosome)):
        if chromosome[i] == 1:
            selected[selected_i] = points[i]
            selected_i += 1
        else:
            non_selected[non_selected_i] = points[i]
            non_selected_i += 1
    
    upperX = max([coord[0] for coord in points]) 
    lowerX = min([coord[0] for coord in points]) 

    upperY = max([coord[1] for coord in points]) 
    lowerY = min([coord[1] for coord in points]) 

    #Given all non-selected points, draw a line between it and the closest selected point.
    for non_selected_point in non_selected:
         selected_point = None
         min_dis = sys.maxsize 
         for possible_point in selected:
            dis = euclidean_distance(non_selected_point, possible_point)
            if (dis < min_dis):
                 selected_point = possible_point
                 min_dis = dis
         plt.plot([non_selected_point[0], selected_point[0]], [non_selected_point[1], selected_point[1]], color='black')

              
    #Plot all points
    plt.plot([x[0] for x in selected], [y[1] for y in selected], 'o', color='red')
    plt.plot([x[0] for x in non_selected], [y[1] for y in non_selected], 'o', color='blue')

    plt.xlim(lowerX-1,upperX+1)
    plt.ylim(lowerY-1,upperY+1)

    plt.xscale('linear')
    plt.yscale('linear')

    filePath = os.path.join(sys.path[0], "Results", "Graphs", file_name + '.png')
    plt.savefig(filePath)
    plt.clf()

def euclidean_distance(curr_city, selected_city):
    x_term = (curr_city[0] - selected_city[0]) ** 2
    y_term = (curr_city[1] - selected_city[1]) ** 2
    return math.sqrt(x_term + y_term)