from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from pandas import DataFrame

import os
import sys

def generate_dataset(p = 3):

    X, y = make_blobs(n_samples=(p*(p+1)), centers=p, n_features=2, cluster_std=p-1, center_box=(0, p*(p+1)))

    df = DataFrame(X)
    filePath = os.path.join(sys.path[0], 'dataset',  'P_{0}_N_{1}.xlsx'.format(int(p), int(p*(p+1))))
    df.to_excel(filePath, sheet_name='Sheet1')