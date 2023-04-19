import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

from pathlib import Path

def load_dataset(p = 4, n = 20):
    file_path = os.path.join(sys.path[0], 'dataset', "P_{0}_N_{1}.xlsx".format(p, n))

    df = pd.read_excel(file_path, engine='openpyxl')
    
    points = np.empty((n, 2))

    #Load in all of the values from the df into a numpy array
    i = 0
    for coord in df.values:
        points[i, 0] = coord[0]
        points[i, 1] = coord[1]
        i += 1

    #Return the matrix of points
    return points

def graph_raw_points(points):
    plt.plot(points[:, 0], points[:, 1], 'o', color='black')
    plt.show()


def save_stats(selection, crossover, mutation, fitness, file_name):
    path = os.path.join(sys.path[0], 'Results', 'Stats', file_name + '.xlsx')
    wb = openpyxl.load_workbook(path) 
    sheet = wb.active 
    sheet.append([selection, crossover, mutation, fitness])
    
    wb.save(path)
