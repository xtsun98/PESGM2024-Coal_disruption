import numpy as np
import pandas as pd
import time
from gurobipy import *

from system_information import sys_info
from projection import updatePrimal, updateDual
from coal_supply_chain_equilibrium import coal_supply_chain_equilibrium
from coal_to_electricity import coal2elec
from electricity_market_clearing import electricity_market_clearing

if __name__ == '__main__':

    disruption_flag_set = {0, 1, 2} # for no disruption, CME outage, and transportation cessation
    disruption_number_set_CME = {1, 2, 3} # CME number
    disruption_number_set_Transp = {1, 2, 3, 4, 5, 6, 7, 8} # freight railway number

    ElecPrice_list = pd.DataFrame(data=None, index=['0']
                                                   +['CME{}'.format(m) for m in range(1, 4)]
                                                   +['Transp{}'.format(e) for e in range(1, 9)],
                                  columns=['ElecPrice'])
    GenCost_list = pd.DataFrame(data=None, index=['0']
                                                 +['CME{}'.format(m) for m in range(1, 4)]
                                                 +['Transp{}'.format(e) for e in range(1, 9)],
                                columns=['Gen{}Cost'.format(g) for g in range(1, 4)])
    GenCapa_list = pd.DataFrame(data=None, index=['0']
                                                 + ['CME{}'.format(m) for m in range(1, 4)]
                                                 + ['Transp{}'.format(e) for e in range(1, 9)],
                                columns=['Gen{}Capa'.format(g) for g in range(1, 4)])

    for disruption_flag in disruption_flag_set:
        if disruption_flag == 0: # no disruption
            rStorage, qStorage, yStorage, dualStorage, maxMoveStorage = coal_supply_chain_equilibrium(disruption_flag, 0)
            GenCost, GenCapa = coal2elec(yStorage)
            for g in range(1, 4):
                GenCost_list.loc['0', 'Gen{}Cost'.format(g)] = GenCost.loc['Price', 'GC{}'.format(g)]
                GenCapa_list.loc['0', 'Gen{}Capa'.format(g)] = GenCapa.loc['Quantity', 'GC{}'.format(g)]
            elecprice = electricity_market_clearing(GenCost, GenCapa)
            ElecPrice_list.loc['0', 'ElecPrice'] = elecprice

        elif disruption_flag == 1: # CME disruption
            for disruption_number in disruption_number_set_CME:
                rStorage, qStorage, yStorage, dualStorage, maxMoveStorage = coal_supply_chain_equilibrium(disruption_flag, disruption_number)
                GenCost, GenCapa = coal2elec(yStorage)
                for g in range(1, 4):
                    GenCost_list.loc['CME{}'.format(disruption_number), 'Gen{}Cost'.format(g)] = GenCost.loc['Price', 'GC{}'.format(g)]
                    GenCapa_list.loc['CME{}'.format(disruption_number), 'Gen{}Capa'.format(g)] = GenCapa.loc['Quantity', 'GC{}'.format(g)]
                elecprice = electricity_market_clearing(GenCost, GenCapa)
                ElecPrice_list.loc['CME{}'.format(disruption_number), 'ElecPrice'] = elecprice

        elif disruption_flag == 2: # Transp cessation
            for disruption_number in disruption_number_set_Transp:
                rStorage, qStorage, yStorage, dualStorage, maxMoveStorage = coal_supply_chain_equilibrium(disruption_flag, disruption_number)
                GenCost, GenCapa = coal2elec(yStorage)
                for g in range(1, 4):
                    GenCost_list.loc['Transp{}'.format(disruption_number), 'Gen{}Cost'.format(g)] = GenCost.loc[
                        'Price', 'GC{}'.format(g)]
                    GenCapa_list.loc['Transp{}'.format(disruption_number), 'Gen{}Capa'.format(g)] = GenCapa.loc[
                        'Quantity', 'GC{}'.format(g)]
                elecprice = electricity_market_clearing(GenCost, GenCapa)
                ElecPrice_list.loc['Transp{}'.format(disruption_number), 'ElecPrice'] = elecprice


