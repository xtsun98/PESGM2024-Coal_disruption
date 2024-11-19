import numpy as np
import pandas as pd
from system_information import sys_info


def coal2elec(yStorage):

    CME, TN, GC = sys_info()

    yResult = pd.DataFrame(data=None, index = ['Quantity'], columns=['GC{}'.format(g) for g in range(1, 4)])
    PIResult = pd.DataFrame(data=None, index=['Price'], columns=['GC{}'.format(g) for g in range(1, 4)])

    for g in range(1, 4):
        yResult.loc['Quantity', 'GC{}'.format(g)] = sum(yStorage.iloc[-1]['GC{}CME{}'.format(g, m)]
                                                        for m in range(1, 4))
        PIResult.loc['Price', 'GC{}'.format(g)] = GC.PImax.loc['MaxPrice', 'GC{}'.format(g)] \
                                                  - GC.beta.loc['Beta', 'GC{}'.format(g)]*yResult.loc['Quantity', 'GC{}'.format(g)]

    GenCost = PIResult
    GenCapa = yResult

    return GenCost, GenCapa