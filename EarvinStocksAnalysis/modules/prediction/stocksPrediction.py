import pandas as pd
import numpy as np

HIGH_SIG = 1
LOW_SIG = -1
CLS_MAX = 2
CLS_MIN = 0
CLS_OBJ = 1

"""
說明：取得高低點訊號區間

待強化項目：
01. 沒有錯誤檢查機制，以後要改進
02. 沒有利用pandas Series的特色寫，以後要改進 
"""
def splitSector(v1, v2) :
    rtnData = []
    i = 0
    sum = 0
    while i < len(v1) :
        if v1.iloc[i] <= v2.iloc[i] :
            rtnData.append(LOW_SIG)
        else :
            rtnData.append(HIGH_SIG)
        i += 1

    return pd.Series(rtnData, index=v1.index)


""" (2023.07.18 Created, not finished)
資料前處理
Input Param :
    indexData   指標資料
    clusterType 聚類模式(望大 CLS_MAX、望小 CLS_MIN、望目 CLS_OBJ)
"""
def preProcess(v, clusterType) :
    rtnData = []
    print("max: ", v.max())
    print("min: ", v.min())
    for i in range(len(v)) :
#        print(v.iloc[i])
        rtnData.append((v.iloc[i]-v.min())/(v.max()-v.min()))

    return pd.Series(rtnData, index=v.index)


""" (2023.07.18 Created, not finished)
開始聚類
grgDF structure
    index : sd.trade_date
    data-collection :
    indexname1_indDay : data_series
    indexname2_indDay : data_series
    ...
sigFlag : 
    HIGH_SIG -> 求高點區間
    LOW_SIG  -> 求低點區間
"""
def execGRG(grgDF, sigFlag) :
    return 0