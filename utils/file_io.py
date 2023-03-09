import sys
import os
import pandas as pd
import numpy as np

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