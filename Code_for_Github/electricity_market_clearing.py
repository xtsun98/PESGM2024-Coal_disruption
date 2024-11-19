import numpy as np
import pandas as pd
import time
from gurobipy import *

def electricity_market_clearing(GenCost, GenCapa):

    shedding_price = 15
    D = 3.25

    model = Model(name='ElectricityMarket')

    p = {} # power of generators
    for g in range(1, 4):
        p[g] = model.addVar(lb=0.0, ub=GenCapa.loc['Quantity', 'GC{}'.format(g)], vtype=GRB.CONTINUOUS, name='p{}'.format(g))
    d = model.addVar(lb=0.0, ub=float('inf'), vtype=GRB.CONTINUOUS, name='d')

    Cons_power_balance = model.addConstr(quicksum(p[g] for g in range(1, 4)) + d == D, name='power balance')

    obj = 0
    for g in range(1, 4):
        obj = obj + GenCost.loc['Price', 'GC{}'.format(g)]*p[g]
    obj = obj + shedding_price*d

    model.setObjective(obj, sense=GRB.MINIMIZE)
    model.update()
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print('*' * 100)
        print('Electricity Market Problem Successfully Solved.')
        elecprice = Cons_power_balance.Pi


    if model.status in {3, 4, 5}:
        print('=' * 100)
        print('Electricity Market Problem Wrong.')
        elecprice = np.nan

    return elecprice