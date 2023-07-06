import pandas as pd

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



"""
技術指標 PSY
input :
    stocksData : 股票資料
    indexDay   : 指標天數
output :
    rtnData    : 回傳技術指標PSY值(Series object)
"""
def indexWMS(sd, indDay) :
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


"""
說    明: 
    VR Index (成交量比率)
    依據「量先於價」及「價量同步同向」之理論，計算一段期間內上漲日交易金
    額與下跌日交易金額之比率關係，以為研依據
    Formula: VR(n) = [UpTotVol(n)+(1/2×EquTotVol(n)] /
                     [DownTotVol(n)+(1/2×EquTotVol(n)] × 100
                     UpTotVol(n)  ：表示過去n日股價上漲日之成交量總數
                     DownTotVol(n)：表示過去n日股價下跌日之成交量總數
                     EquTotVol(n) ：表示過去n日股價不變日之成交量總數
輸入參數: 
    udtStock   股市資料
    udtIndex   股市指標資料
    intStockNo 股市資料的筆數
    intVRNo    欲計算指標之天數
輸出參數: 無
版    本: 
    1.00 20130706 新增
"""
def indexVR(sd, indDay) :
#    print("=== Calculate index VR ===")
#    print("the data size is ", len(sd))
    sdStartPrice = list(sd.start_price)
    sdEndPrice = list(sd.end_price)
    sdVolume = list(sd.volume)
    rtnData = []
    i = 0

    while i < len(sdEndPrice) :
        if i < (indDay - 1) :
            rtnData.append(0)
        else :
            k = i
            volumeUp = 0
            volumeDown = 0
            volumeFlat = 0
            for j in range(0,indDay) :
#                print("k= ", k, ", i= ", i, ",up= ", up)
                if (sdEndPrice[k] - sdStartPrice[k]) > 0 :
                    volumeUp += sdVolume[k]
                elif (sdEndPrice[k] - sdStartPrice[k]) < 0 :
                    volumeDown += sdVolume[k]
                else :
                    volumeFlat += sdVolume[k]
                k = k - 1
            
            if (volumeUp + volumeDown + (volumeFlat / 2)) > 0 :
                rtnData.append(((volumeUp + (volumeFlat / 2))/(volumeUp + volumeDown + (volumeFlat / 2)))*100)
            else :
                rtnData.append(0)
            
        i = i + 1

    return pd.Series(rtnData, index=sd.trade_date) 

