import matplotlib
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm

if __name__ == '__main__':

    disruption_name = ['None']+['CME{}'.format(m) for m in range(1, 4)]+['Transp{}'.format(e) for e in range(1, 9)]
    load_level = [1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25]

    ElecPrice = pd.read_excel('Results/impact.xlsx', sheet_name='Sheet1', index_col=0)
    minPrice = ElecPrice.values.min()
    NormalizedElecPrice = np.array(ElecPrice / minPrice).transpose()

    fig, ax = plt.subplots()
    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    # plt.grid(visible=True, axis='both', linewidth=0.5)
    im = ax.imshow(NormalizedElecPrice, cmap='bwr', alpha=0.7)

    ax.set_yticks(np.arange(len(load_level)), labels=load_level)
    ax.set_xticks(np.arange(len(disruption_name)), labels=disruption_name)

    for i in range(len(load_level)):
        for j in range(len(disruption_name)):
            text = ax.text(j, i, str(NormalizedElecPrice[i, j])[0:4],
                           ha="center", va="center", color="k")


    plt.show()

