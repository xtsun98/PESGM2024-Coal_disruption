import numpy as np
import pandas as pd

def sys_info():
    class CME:
        def __init__(self, Rmax, CM, AM):
            self.Rmax = Rmax    # max production
            self.CM = CM        # production cost
            self.AM = AM        # location of CME
    Rmax = pd.read_excel('Case Data/CME_info.xlsx', sheet_name='Production', index_col=0)
    CM = pd.read_excel('Case Data/CME_info.xlsx', sheet_name='Cost', index_col=0)
    AM = pd.read_excel('Case Data/CME_info.xlsx', sheet_name='Location', index_col=0)
    AM.fillna(0, inplace=True)
    CME = CME(Rmax, CM, AM)

    class TN:
        def __init__(self, B, CT, Qmax, Q0):
            self.B = B          # incidence matrix
            self.CT = CT        # transportation cost
            self.Qmax = Qmax    # transportation capacity
            self.Q0 = Q0        # discount
    B = pd.read_excel('Case Data/TN_info.xlsx', sheet_name='IncidenceMatrix', index_col=0)
    B.fillna(0, inplace=True)
    CT = pd.read_excel('Case Data/TN_info.xlsx', sheet_name='Cost', index_col=0)
    Qmax = pd.read_excel('Case Data/TN_info.xlsx', sheet_name='Capacity', index_col=0)
    Q0 = pd.read_excel('Case Data/TN_info.xlsx', sheet_name='Discount', index_col=0)
    TN = TN(B, CT, Qmax, Q0)

    class GC:
        def __init__(self, Ymax, PImax, Beta, AG):
            self.Ymax = Ymax        # coal capacity of GenCo
            self.PImax = PImax      # max coal price of GenCo
            self.beta = Beta        # price-quantitiy sensitivity
            self.AG = AG            # location of GenCo
    Ymax = pd.read_excel('Case Data/GC_info.xlsx', sheet_name='Capacity', index_col=0)
    PImax = pd.read_excel('Case Data/GC_info.xlsx', sheet_name='MaxPrice', index_col=0)
    Beta = pd.read_excel('Case Data/GC_info.xlsx', sheet_name='Beta', index_col=0)
    AG = pd.read_excel('Case Data/GC_info.xlsx', sheet_name='Location', index_col=0)
    AG.fillna(0, inplace=True)
    GC = GC(Ymax, PImax, Beta, AG)

    return CME, TN, GC

if __name__ == '__main__':
    CME, TN, GC = sys_info()