import pandas as pd
#import modules.db.StocksData as sd


def testMAP(x) :
    print(x)

def testMAP2(x) :
    theResult = sd.GetStocksData("0056")
    return theResult

"""
技術指標 MAP
input :
    stocksData : 股票資料
    indexDay   : 指標天數
output :
    rtnData    : 回傳技術指標MAP值(Series object)
"""
def indexMAP(sd, indDay) :
#    print("=== Calculate index map ===")
#    print("the data size is ", len(sd))
    sdEndPrice = list(sd.end_price)
    rtnData = []
    i = 0
    sum = 0
    while i < len(sdEndPrice) :
        if i < (indDay - 1) :
            rtnData.append(0)
            sum += sdEndPrice[i]
        else :
            while i < len(sdEndPrice) :
                sum += sdEndPrice[i]
                rtnData.append(sum / indDay)
                sum = sum - sdEndPrice[i-indDay+1]
                i += 1
        i += 1

    return pd.Series(rtnData, index=sd.trade_date)
