import pandas as pd
#import modules.db.StocksData as sd



"""
技術指標 PSY
input :
    stocksData : 股票資料
    indexDay   : 指標天數
output :
    rtnData    : 回傳技術指標PSY值(Series object)
"""
def indexPSY(sd, indDay) :
#    print("=== Calculate index PSY ===")
#    print("the data size is ", len(sd))
    sdEndPrice = list(sd.end_price)
    rtnData = []
    i = 0
    up = 0

    while i < len(sdEndPrice) :
        if i < (indDay - 1) :
            rtnData.append(50)
        else :
            k = i
            up = 0
            for j in range(0,indDay) :
#                print("k= ", k, ", i= ", i, ",up= ", up)
                if sdEndPrice[k] - sdEndPrice[k-1] > 0 :
                    up = up + 1
                k = k - 1
            rtnData.append(up/indDay*100)
        i = i + 1

    return pd.Series(rtnData, index=sd.trade_date)
