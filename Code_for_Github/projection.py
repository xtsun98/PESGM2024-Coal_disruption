import numpy as np
import pandas as pd
from gurobipy import *

from system_information import sys_info


def updatePrimal(CME, TN, GC, rStorage, qStorage, yStorage, dualStorage, delta, k, m, disruption_flag, disruption_number):
    # disruption flag: 1 --> CME outage
    #                  2 --> transportation cessation
    #                  0 --> no outage
    # disruption number: CME outage --> 1, 2, 3
    #                    transportation cessation --> 1, ..., 8

    # find r of last iteration
    rOld = rStorage.loc[k - 1, 'CME{}'.format(m)]
    # find q of last iteration
    qOld = pd.DataFrame(data=None, index=['E{}'.format(e) for e in range(1, 17)],
                        columns=['CME{}'.format(mm) for mm in range(1, 4)])
    for e in range(1, 17):
        for mm in range(1, 4):
            qOld.loc['E{}'.format(e), 'CME{}'.format(mm)] = qStorage.loc[k - 1, 'E{}CME{}'.format(e, mm)]
    # find y of last iteration
    yOld = pd.DataFrame(data=None, index=['GC{}'.format(g) for g in range(1, 4)],
                        columns=['CME{}'.format(mm) for mm in range(1, 4)])
    for g in range(1, 4):
        for mm in range(1, 4):
            yOld.loc['GC{}'.format(g), 'CME{}'.format(mm)] = yStorage.loc[k - 1, 'GC{}CME{}'.format(g, mm)]
    # find dual multiplier fo last iteration
    dualOld = pd.DataFrame(data=None, index=['GC{}'.format(g) for g in range(1, 4)],
                           columns=['CME{}'.format(mm) for mm in range(1, 4)])
    for g in range(1, 4):
        for mm in range(1, 4):
            dualOld.loc['GC{}'.format(g), 'CME{}'.format(mm)] = dualStorage.loc[k - 1, 'GC{}CME{}'.format(g, mm)]

    # linearly constrained quadratic programming projection
    model = Model(name='Primal_Update_Iter{}_CME{}'.format(k, m))

    r = model.addVar(lb=0.0, ub=CME.Rmax.loc['Production', 'CME{}'.format(m)], vtype=GRB.CONTINUOUS, name='r')
    q = {}
    y = {}
    for e in range(1, 17):
        q[e] = model.addVar(lb=0.0, ub=TN.Qmax.loc['Capacity', 'E{}'.format(e)], vtype=GRB.CONTINUOUS)
    for g in range(1, 4):
        y[g] = model.addVar(lb=0.0, ub=GC.Ymax.loc['Capacity', 'GC{}'.format(g)], vtype=GRB.CONTINUOUS)

    for l in range(1, 8):
        model.addConstr(quicksum(TN.B.loc['L{}'.format(l), 'E{}'.format(e)] * q[e]
                                 for e in range(1, 17))
                        + CME.AM.loc['L{}'.format(l), 'CME{}'.format(m)] * r
                        == quicksum(GC.AG.loc['L{}'.format(l), 'GC{}'.format(g)] * y[g]
                                    for g in range(1, 4)), name='nodal_balance{}'.format(l))

    # disruption constraints
    if disruption_flag == 1: # CME m outage
        if m == disruption_number:
            model.addConstr(r == 0, name='CME{}_disruption'.format(m))
    elif disruption_flag == 2: # transportation network e cessation
        model.addConstr(q[disruption_number*2-1] == 0, name='E{}_disruption'.format(disruption_number*2-1))
        model.addConstr(q[disruption_number*2] == 0, name='E{}_disruption'.format(disruption_number*2))

    objR = 0  # square error of r
    objQ = 0  # square error of q
    objY = 0  # square error of y

    objR = objR + (r - rOld - delta * CME.CM.loc['Cost', 'CME{}'.format(m)]) * (
                r - rOld - delta * CME.CM.loc['Cost', 'CME{}'.format(m)])
    for e in range(1, 17):
        objQ = objQ + (q[e] - qOld.loc['E{}'.format(e), 'CME{}'.format(m)]
                       + delta * TN.CT.loc['Cost', 'E{}'.format(e)]
                       * (1-TN.Q0.loc['Discount', 'E{}'.format(e)]
                          /(TN.Q0.loc['Discount', 'E{}'.format(e)]+qOld.loc['E{}'.format(e), 'CME{}'.format(m)])
                          /(TN.Q0.loc['Discount', 'E{}'.format(e)]+qOld.loc['E{}'.format(e), 'CME{}'.format(m)]))) \
               * (q[e] - qOld.loc['E{}'.format(e), 'CME{}'.format(m)]
                  + delta * TN.CT.loc['Cost', 'E{}'.format(e)]
                  * (1-TN.Q0.loc['Discount', 'E{}'.format(e)]
                     /(TN.Q0.loc['Discount', 'E{}'.format(e)]+qOld.loc['E{}'.format(e), 'CME{}'.format(m)])
                     /(TN.Q0.loc['Discount', 'E{}'.format(e)]+qOld.loc['E{}'.format(e), 'CME{}'.format(m)])))

    for g in range(1, 4):
        objY = objY + (y[g] - yOld.loc['GC{}'.format(g), 'CME{}'.format(m)]
                       - delta * (GC.PImax.loc['MaxPrice', 'GC{}'.format(g)]
                                  - GC.beta.loc['Beta', 'GC{}'.format(g)] * (
                                              y[g] + sum(yOld.loc['GC{}'.format(g), 'CME{}'.format(mm)]
                                                         for mm in range(1, 4)))
                                  + dualOld.loc['GC{}'.format(g), 'CME{}'.format(m)])) \
               * (y[g] - yOld.loc['GC{}'.format(g), 'CME{}'.format(m)]
                  - delta * (GC.PImax.loc['MaxPrice', 'GC{}'.format(g)]
                             - GC.beta.loc['Beta', 'GC{}'.format(g)] * (
                                         y[g] + sum(yOld.loc['GC{}'.format(g), 'CME{}'.format(mm)]
                                                    for mm in range(1, 4)))
                             + dualOld.loc['GC{}'.format(g), 'CME{}'.format(m)]))
    obj = objR + objQ + objY


    model.setParam('OutputFlag', 0)
    model.setObjective(obj, sense=GRB.MINIMIZE)
    model.update()
    # model.write('LP/Primal_Update_Iter{}_CME{}.lp'.format(k, m))

    model.optimize()

    if model.status == GRB.OPTIMAL:
        print('*' * 100)
        print('Primal_Update_Iter{}_CME{}==Successfully Solved.'.format(k, m))

        rStorage.loc[k, 'CME{}'.format(m)] = r.X
        for e in range(1, 17):
            qStorage.loc[k, 'E{}CME{}'.format(e, m)] = q[e].X

        for g in range(1, 4):
            yStorage.loc[k, 'GC{}CME{}'.format(g, m)] = y[g].X

    if model.status in {3, 4, 5}:
        print('=' * 100)
        print('Primal_Update_Iter{}_CME{}==Wrong.'.format(k, m))

    return rStorage, qStorage, yStorage

def updateDual(GC, yStorage, dualStorage, delta, k, g):
    # find y of last iteration
    yOld = pd.DataFrame(data=None, index=['GC{}'.format(g) for g in range(1, 4)],
                        columns=['CME{}'.format(mm) for mm in range(1, 4)])
    for mm in range(1, 4):
        yOld.loc['GC{}'.format(g), 'CME{}'.format(mm)] = yStorage.loc[k, 'GC{}CME{}'.format(g, mm)]
    # find dual multiplier of last iteration
    dualOld = pd.DataFrame(data=None, index=['GC{}'.format(g) for g in range(1, 4)],
                           columns=['CME{}'.format(mm) for mm in range(1, 4)])
    for mm in range(1, 4):
        dualOld.loc['GC{}'.format(g), 'CME{}'.format(mm)] = dualStorage.loc[k-1, 'GC{}CME{}'.format(g, mm)]

    # update dual in gradient direction
    dual = pd.DataFrame(data=None, index=['GC{}'.format(g)],
                        columns=['CME{}'.format(mm) for mm in range(1, 4)])
    for mm in range(1, 4):
        dual.loc['GC{}'.format(g), 'CME{}'.format(mm)] = dualOld.loc['GC{}'.format(g), 'CME{}'.format(mm)] \
                                                        + delta*(GC.Ymax.loc['Capacity', 'GC{}'.format(g)]
                                                                 - sum(yOld.loc['GC{}'.format(g), 'CME{}'.format(mm)]
                                                                       for mm in range(1, 4)))
        # projection onto positive half-plane
        if dual.loc['GC{}'.format(g), 'CME{}'.format(mm)] < 0:
            dual.loc['GC{}'.format(g), 'CME{}'.format(mm)] = 0

        dualStorage.loc[k, 'GC{}CME{}'.format(g, mm)] = dual.loc['GC{}'.format(g), 'CME{}'.format(mm)]

    return dualStorage



