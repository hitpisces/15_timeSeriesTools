# -*- coding: utf-8 -*-
# @Time    : 20/3/10 15:38
# @Author  : Jay Lam
# @File    : Auto-ARIMA.py
# @Software: PyCharm


import numpy as np
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=(FutureWarning, UserWarning))
import math
import pyramid as pm
import pymysql
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error


# 将单井、单指标数据从数据库中提取成单列并存到csv文件中
def sqlExtra(path):
    idCode = ['PG-40']
    indexCode = ['AlK']

    for x in idCode:
        for y in indexCode:
            writer = pd.ExcelWriter(path + x + "井的" + y + "指标筛选结果.xlsx")
            db = pymysql.connect("localhost", "root", "sustc@10", "pggroundwater")
            cursor = db.cursor()
            sqlStr = "SELECT `st`,`" + y + "` FROM `pg1018` WHERE `wellno` = \'" + x + "\'"
            cursor.execute(sqlStr)
            sqlResults = cursor.fetchall()

            columnDes = cursor.description
            columnNames = [columnDes[i][0] for i in range(len(columnDes))]
            df = pd.DataFrame([list(i) for i in sqlResults], columns=columnNames)
            # df.drop('st',axis=1,inplace=True)

    result = df.values.tolist()
    return result


# 判断序列中指定字符出现和结束的位置
def strLocator(inputList, targetStr):
    result = []
    for i, x in enumerate(inputList):
        if x == targetStr:
            result.append(i)
    return result


# 使用Auto-ARIMA预测后续N点数值
def autoARIMA(inputDataSet, n):
    inputData = inputDataSet.astype(np.float64)
    stepwise_fit = pm.auto_arima(inputData, start_p=1, start_q=1,
                                 max_p=3, max_q=3, m=12,
                                 start_P=0, seasonal=True,
                                 d=1, D=1, trace=True,
                                 error_action='ignore',  # don't want to know if an order does not work
                                 suppress_warnings=True,  # don't want convergence warnings
                                 stepwise=True)  # set to stepwise
    return stepwise_fit.predict(n)


# rms = math.sqrt(mean_squared_error(valid, forecast))
if __name__ == '__main__':
    print(sqlExtra("C:\\"))
