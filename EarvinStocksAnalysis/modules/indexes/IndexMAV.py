import pandas as pd
#import modules.db.StocksData as sd

"""
技術指標 MAV
input :
    stocksData : 股票資料
    indexDay   : 指標天數
output :
    rtnData    : 回傳技術指標MAV值(Series object)
"""
def indexMAV(sd, indDay) :
#    print("=== Calculate index map ===")
#    print("the data size is ", len(sd))
    sdVolume = list(sd.volume)
    rtnData = []
    i = 0
    sum = 0
    while i < len(sdVolume) :
        if i < (indDay - 1) :
            rtnData.append(0)
            sum += sdVolume[i]
        else :
            while i < len(sdVolume) :
                sum += sdVolume[i]
                rtnData.append(sum / indDay)
                sum = sum - sdVolume[i-indDay+1]
                i += 1
        i += 1

    return pd.Series(rtnData, index=sd.trade_date)
