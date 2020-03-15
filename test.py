# -*- coding: utf-8 -*-
# @Time    : 20/3/14 0:19
# @Author  : Jay Lam
# @File    : test.py
# @Software: PyCharm


import numpy as np
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=(FutureWarning,UserWarning))
import pyramid as pm
from pyramid.datasets import load_wineind

# this is a dataset from R
wineind = pd.read_csv('pg43.csv').astype(np.float64)
#wineind =wineind = load_wineind().astype(np.float64)


# fit stepwise auto-ARIMA
stepwise_fit = pm.auto_arima(wineind, start_p=1, start_q=1,
                             max_p=3, max_q=3, m=12,
                             start_P=0, seasonal=True,
                             d=1, D=1, trace=True,
                             error_action='ignore',  # don't want to know if an order does not work
                             suppress_warnings=True,  # don't want convergence warnings
                             stepwise=True)  # set to stepwise


#print(stepwise_fit.summary())
print(type(stepwise_fit.predict(3)))