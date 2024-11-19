import matplotlib
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm

if __name__ == '__main__':
    r = pd.read_excel('Results/R8-disruption.xlsx', sheet_name='r', index_col=0)
    q = pd.read_excel('Results/R8-disruption.xlsx', sheet_name='q', index_col=0)
    y = pd.read_excel('Results/R8-disruption.xlsx', sheet_name='y', index_col=0)
    dual = pd.read_excel('Results/R8-disruption.xlsx', sheet_name='dual', index_col=0)
    maxMove = pd.read_excel('Results/R8-disruption.xlsx', sheet_name='maxMove', index_col=0)

    rResult = pd.DataFrame(data=None, index=['r'],
                           columns=['CME{}'.format(m) for m in range(1, 4)])
    qResult = pd.DataFrame(data=None, index=['E{}'.format(e) for e in range(1, 15)],
                           columns=['CME{}'.format(m) for m in range(1, 4)])
    yResult = pd.DataFrame(data=None, index=['GC{}'.format(g) for g in range(1, 4)],
                           columns=['CME{}'.format(m) for m in range(1, 4)])

    for m in range(1, 4):
        rResult.loc['r', 'CME{}'.format(m)] = r.iloc[-1]['CME{}'.format(m)]
        for e in range(1, 15):
            qResult.loc['E{}'.format(e), 'CME{}'.format(m)] = q.iloc[-1]['E{}CME{}'.format(e, m)]
        for g in range(1, 4):
            yResult.loc['GC{}'.format(g), 'CME{}'.format(m)] = y.iloc[-1]['GC{}CME{}'.format(g, m)]

    # Sample data for the stacked bar graph
    categories = ['GC1', 'GC2', 'GC3']
    yGC1 = np.array([yResult.loc['GC1', 'CME1'], yResult.loc['GC1', 'CME2'], yResult.loc['GC1', 'CME3']])
    yGC2 = np.array([yResult.loc['GC2', 'CME1'], yResult.loc['GC2', 'CME2'], yResult.loc['GC2', 'CME3']])
    yGC3 = np.array([yResult.loc['GC3', 'CME1'], yResult.loc['GC3', 'CME2'], yResult.loc['GC3', 'CME3']])

    # Sample data for the line plot
    x = np.arange(len(categories))
    # line_values = [50, 150, 100]

    # Create a figure and two subplots
    # sns.set_style(style='whitegrid')
    # plt.figure(1)
    # plt.tick_params(axis='x', direction='in')
    # plt.tick_params(axis='y', direction='in')
    # plt.ylim([0, 1.5])
    #
    # plt.grid(visible=True, axis='both', linewidth=0.5)
    #
    # # Create the stacked bar graph on the first subplot
    # plt.bar(x, yGC1, label='yGC1', alpha=1, width=0.4, edgecolor='none')
    # plt.bar(x, yGC2, label='yGC2', alpha=1, width=0.4, edgecolor='none', bottom=yGC1)
    # plt.bar(x, yGC3, label='yGC3', alpha=1, width=0.4, edgecolor='none', bottom=yGC1+yGC2)
    #
    # # Set the labels and legend for the stacked bar graph
    # plt.legend()
    # # Show the combined plot
    # plt.tight_layout()
    # plt.show()
    #
    # qCME1 = np.array(qResult.loc[:, 'CME1'])
    # qCME1 = np.where(np.abs(qCME1) < 0.001, 0, qCME1)
    # qCME1_pos = np.array([qCME1[n] for n in {0, 2, 4, 6, 8, 10, 12}])
    # qCME1_neg = np.array([qCME1[n] for n in {1, 3, 5, 7, 9, 11, 13}])
    # qCME2 = np.array(qResult.loc[:, 'CME2'])
    # qCME2 = np.where(np.abs(qCME2) < 0.001, 0, qCME2)
    # qCME2_pos = np.array([qCME2[n] for n in {0, 2, 4, 6, 8, 10, 12}])
    # qCME2_neg = np.array([qCME2[n] for n in {1, 3, 5, 7, 9, 11, 13}])
    # qCME3 = np.array(qResult.loc[:, 'CME3'])
    # qCME3 = np.where(np.abs(qCME3) < 0.001, 0, qCME3)
    # qCME3_pos = np.array([qCME3[n] for n in {0, 2, 4, 6, 8, 10, 12}])
    # qCME3_neg = np.array([qCME3[n] for n in {1, 3, 5, 7, 9, 11, 13}])
    #
    # #
    # #
    # #
    # sns.set_style(style='whitegrid')
    # plt.figure(2)
    # plt.tick_params(axis='x', direction='in')
    # plt.tick_params(axis='y', direction='in')
    # plt.grid(visible=True, axis='both', linewidth=0.5)
    # classes = ['E{}'.format(e) for e in range(1, 8)]
    # x = np.arange(len(classes))
    # plt.bar(x, -qCME3_neg, label='qCME3_neg', color='C2', width=0.2, edgecolor='none', bottom=-0)
    # plt.bar(x, -qCME2_neg, label='qCME2_neg', facecolor='C1', width=0.2, edgecolor='none', bottom=-qCME3_neg)
    # plt.bar(x, -qCME1_neg, label='qCME1_neg', facecolor='C0', width=0.2, edgecolor='none', bottom=-qCME3_neg-qCME2_neg)
    # plt.bar(x, qCME1_pos, label='qCME1_pos', facecolor='C0', width=0.2, edgecolor='none', bottom=0)
    # plt.bar(x, qCME2_pos, label='qCME2_pos', facecolor='C1', width=0.2, edgecolor='none', bottom=qCME1_pos)
    # plt.bar(x, qCME3_pos, label='qCME3_pos', facecolor='C2', width=0.2, edgecolor='none', bottom=qCME1_pos+qCME2_pos)
    #
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    sns.set_style(style='whitegrid')
    fig, ax1 = plt.subplots()
    ax1.tick_params(axis='x', direction='in')
    ax1.tick_params(axis='y', direction='in')
    ax1.grid(visible=True, axis='both', linewidth=0.5)

    ax1.plot(np.arange(len(r.loc[:, 'CME1'])), np.array(r.loc[:, 'CME1']), label='rCME1', color='C0')
    ax1.plot(np.arange(len(y.loc[:, 'GC1CME1'])), np.array(y.loc[:, 'GC1CME1']), label='yGC1CME1', color='C1')
    ax1.plot(np.arange(len(q.loc[:, 'E4CME3'])), np.array(q.loc[:, 'E4CME3']), label='qE4CME3', color='C2')
    ax1.plot(np.arange(len(dual.loc[:, 'GC2CME2'])), np.array(dual.loc[:, 'GC2CME2']), label='dualGC2CME2', color='C3')

    ax2 = ax1.twinx()
    ax2.tick_params(axis='y', direction='in', which='both')
    ax2.set_yscale('log')
    ax2.plot(np.arange(len(maxMove.loc[:, 'gap'])), np.array(maxMove.loc[:, 'gap']), label='gap', color='C4', linestyle='--')

    ax1.legend()
    ax2.legend()

    plt.xlim([0, 300])

    plt.show()



