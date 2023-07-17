import pandas as pd
import numpy as np

HIGH_SIG = 1
LOW_SIG = -1

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

