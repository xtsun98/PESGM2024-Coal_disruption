#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 13:54:58 2023

@author: xtsun
"""

import numpy as np
import pandas as pd
import time
from gurobipy import *

from system_information import sys_info
from projection import updatePrimal, updateDual



if __name__ == '__main__':

    # load system information
    CME, TN, GC = sys_info()

    # initialization settings
    rIni = 1          # production
    qIni = 0          # transportation
    yIni = 0.2          # sale
    dualIni = 0.5       # dual multiplier
    delta = 0.01      # update step
    epsilon = 0.001    # convergence criterion
    kmax = 2000        # maximum iteration

    # solution storage
    rStorage = pd.DataFrame(data=None, index=[k for k in range(kmax+1)],
                            columns=['CME{}'.format(m) for m in range(1, 4)])
    qStorage = pd.DataFrame(data=None, index=[k for k in range(kmax+1)],
                            columns=['E{}CME{}'.format(e, m)
                                       for e in range(1, 17) for m in range(1, 4)])
    yStorage = pd.DataFrame(data=None, index=[k for k in range(kmax+1)],
                            columns=['GC{}CME{}'.format(g, m)
                                     for g in range(1, 4) for m in range(1, 4)])
    dualStorage = pd.DataFrame(data=None, index=[k for k in range(0, kmax+1)],
                               columns=['GC{}CME{}'.format(g, m)
                                        for g in range(1, 4) for m in range(1, 4)])
    maxMoveStorage = pd.DataFrame(data=None, index=[k for k in range(0, kmax+1)],
                                  columns=['gap'])

    # start iteration
    start_time = time.time()
    for k in range(kmax+1):
        print('&'*100)
        print('Iteration {} Starts.'.format(k))
        if k == 0:
            for m in range(1, 4):
                rStorage.loc[0, 'CME{}'.format(m)] = rIni
                for e in range(1, 17):
                    qStorage.loc[0, 'E{}CME{}'.format(e, m)] = qIni
                for g in range(1, 4):
                    yStorage.loc[0, 'GC{}CME{}'.format(g, m)] = yIni
                    dualStorage.loc[0, 'GC{}CME{}'.format(g, m)]  = dualIni
        else:
            # update primal x=(r,q,y)
            for m in range(1, 4):
                print('+++++Primal Problem {}++++++'.format(m))
                rStorage, qStorage, yStorage = updatePrimal(CME, TN, GC, rStorage, qStorage, yStorage, dualStorage, delta, k, m, 1, 8)

            # update dual
            for g in range(1, 4):
                dualStorage = updateDual(GC, yStorage, dualStorage, delta, k, g)

            # check convergence
            rMove = pd.DataFrame(data=None, index=[k], columns=['CME{}'.format(m) for m in range(1, 4)])
            qMove = pd.DataFrame(data=None, index=[k], columns=['E{}CME{}'.format(e, m)
                                                                     for e in range(1, 17) for m in range(1, 4)])
            yMove = pd.DataFrame(data=None, index=[k], columns=['GC{}CME{}'.format(g, m)
                                                                     for g in range(1, 4) for m in range(1, 4)])
            dualMove = pd.DataFrame(data=None, index=[k], columns=['GC{}CME{}'.format(g, m) 
                                                                        for g in range(1, 4) for m in range(1, 4)])
            for m in range(1, 4):
                rMove.loc[k, 'CME{}'.format(m)] = rStorage.loc[k, 'CME{}'.format(m)] \
                                                  - rStorage.loc[k-1, 'CME{}'.format(m)]
                for e in range(1, 17):
                    qMove.loc[k, 'E{}CME{}'.format(e, m)] = qStorage.loc[k, 'E{}CME{}'.format(e, m)] \
                                                            - qStorage.loc[k, 'E{}CME{}'.format(e, m)]
                for g in range(1, 4):
                    yMove.loc[k, 'GC{}CME{}'.format(g, m)] = yStorage.loc[k, 'GC{}CME{}'.format(g, m)] \
                                                             - yStorage.loc[k-1, 'GC{}CME{}'.format(g, m)]
                    dualMove.loc[k, 'GC{}CME{}'.format(g, m)] = dualStorage.loc[k, 'GC{}CME{}'.format(g, m)] \
                                                             - dualStorage.loc[k-1, 'GC{}CME{}'.format(g, m)]
            rMoveMax = rMove.abs().values.max()
            qMoveMax = qMove.abs().values.max()
            yMoveMax = yMove.abs().values.max()
            dualMoveMax = dualMove.abs().values.max()
            maxMoveMax = max([rMoveMax, qMoveMax, yMoveMax, dualMoveMax])
            maxMoveStorage.loc[k, 'gap'] = maxMoveMax
            if maxMoveMax <= epsilon:
                print('#'*100)
                print('Converge at iteration {}'.format(k))
                break
    
    end_time = time.time()
    run_time = end_time - start_time
    print(run_time)

    rStorage.dropna(inplace=True)
    qStorage.dropna(inplace=True)
    yStorage.dropna(inplace=True)
    dualStorage.dropna(inplace=True)
    maxMoveStorage.dropna(inplace=True)

    # output simulation results
    with pd.ExcelWriter('Results/R8-disruption.xlsx', engine='xlsxwriter') as writer:
        rStorage.to_excel(writer, sheet_name='r')
        qStorage.to_excel(writer, sheet_name='q')
        yStorage.to_excel(writer, sheet_name='y')
        dualStorage.to_excel(writer, sheet_name='dual')
        maxMoveStorage.to_excel(writer, sheet_name='maxMove')