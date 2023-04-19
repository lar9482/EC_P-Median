from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from pandas import DataFrame

def generate_dataset(p = 3):
    X, y = make_blobs(n_samples=(p*(p+1)), centers=p, n_features=2, cluster_std=p-1, center_box=(0, p*(p+1)))
    # scatter plot, dots colored by class value
    print(X[:])
    df = DataFrame(dict(x=X[:,0], y=X[:,1], label=y))
    colors = {}
    for c_i in range(0, p):
        colors[c_i] = (c_i/p, 0.25, 0.75)
    # colors = {0:'red', 1:'blue', 2:'green', 3:'yellow', 4:(0.1, 0.1, 0.1)}
    fig, ax = plt.subplots()
    grouped = df.groupby('label')
    for key, group in grouped:
        group.plot(ax=ax, kind='scatter', x='x', y='y', label=key, color=colors[key])
    plt.show()

    
