#coding=ISO-8859-2
#Bollinger band for automated trading
from dateutil import parser
import get_instument as hist
import numpy as np 
import os
import pandas as pd

indicator = 'bollinger'
bollinger_mb = []
bollinger_lb = []
bollinger_ub = []
bollinger_stdev = []

def BollingerBand(date, base, high, low, offset, std_multiplier=2):
    global bollinger_mb, bollinger_lb, bollinger_ub
    bollinger_mb = []
    bollinger_lb = []
    bollinger_ub = []
    bollinger_stdev = []
    bollinger_mb = (moving_average(base, n=offset ))

    data = pd.DataFrame(np.column_stack([date, base, bollinger_mb,high, low]),
                        columns=['date', 'price', 'kvonal', 'high', 'low'])


    data['stdev'] = (data['price'].rolling(offset).std())

    for i in range(0, len(data)):

        if i >= offset :
            bollinger_ub.append(float(data['kvonal'].at[i]) + (float(data['stdev'].at[i])*std_multiplier))
            bollinger_lb.append(float(data['kvonal'].at[i]) - (float(data['stdev'].at[i])*std_multiplier))
            bollinger_stdev.append(float(data['stdev'].at[i])*std_multiplier)
        else:
            bollinger_ub.append(np.nan)
            bollinger_lb.append(np.nan)
            bollinger_stdev.append(np.nan)


    data['felso'] = bollinger_ub
    data['also'] = bollinger_lb
    data['stdev'] = bollinger_stdev

    return data
def moving_average(a, n=12):

    cumsum, moving_aves = [0], []

    for i, x in enumerate(a, 1):
        cumsum.append(cumsum[i - 1] + float(x))
        if i >  n:
            moving_ave = (cumsum[i] - cumsum[i - n]) / n
            moving_aves.append(moving_ave)
        else:
            moving_aves.append(np.nan)
    return moving_aves
def createDatasetForLinearData(dataset, offset = 0):
    dr = []
    index = 1
    for f in dataset:
        if index >= offset:
            dr.append(f)
        else:
            dr.append(f)
        index = index + 1
    return dr


def SetIndicator(ind_setter):
    indicator = ind_setter
def GetIndicator():
    return indicator
def cleanData():
    global bollinger_mb,bollinger_lb,bollinger_ub,bollinger_stdev


    bollinger_mb = []
    bollinger_lb = []
    bollinger_ub = []
    bollinger_stdev = []
