import pandas as pd
import numpy as np

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
    sd      股市資料
    indDay  欲計算指標之天數
輸出參數: rntData   回傳指標值(Series object)
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


"""
說    明:  Calculate the KD values
    K : 「快速平均值」、快線
    D : 「慢速平均值」、慢線
    Formula: KD(n) = 
    [KD]
    today's K = 2/3 yesterday K + 1/3 today RSV
    today's D = 2/3 yesterday D + 1/3 today RSV
    [RSV]
            (今天收盤價 - 最近N天最低價)
    RSV = -------------------------------- * 100
           (最近N天最高價 - 最近N天最低價)
輸入參數: 
    sd      股市資料
    indDay  欲計算指標之天數
輸出參數: dictory {TradeDate, K, D, RSV}
版    本: 
    1.00 20130706 新增(Test OK)
"""
def indexKD(sd, indDay) :
#    print("=== Calculate index KD ===")
#    print("the data size is ", len(sd))
    sdHighPrice = list(sd.high_price)
    sdLowPrice = list(sd.low_price)
    sdEndPrice = list(sd.end_price)
    lstK = []
    lstD =[]
    lstRSV = []
    
    i = 0
    preK = 50
    preD = 50

    while i < len(sdEndPrice) :
        maxValue = -1
        minValue = 99999

        if i < (indDay - 1) :
            # unfinished
            maxValue = max(sdHighPrice[0:i+1])
            minValue = min(sdLowPrice[0:i+1])
        else :
            # unfinished
            maxValue = max(sdHighPrice[(i-indDay+1):(i+1)])
            minValue = min(sdLowPrice[(i-indDay+1):(i+1)])

        rsv = 50
        if maxValue != minValue :
            rsv = (sdEndPrice[i] - minValue) / (maxValue - minValue) * 100

        curK = preK * 2 / 3 + rsv / 3
        curD = preD * 2 / 3 + curK / 3
        lstK.append(curK)
        lstD.append(curD)
        lstRSV.append(rsv)
        preK = curK
        preD = curD
            
        i = i + 1

#    return pd.Series(rtnData, index=sd.trade_date) 
    return {"TradeDate" : sd.trade_date, "K" : lstK, "D" : lstD, "RSV" : lstRSV}


"""
說    明: Calculate the BIAS value
    Formula : 乖離率 = (股價 - 移動平均價) / 移動平均價
輸入參數: 
    sd      股市資料
    indDay  欲計算指標之天數
輸出參數: the BIAS list
版    本: 
    1.00 20130711 新增 (OK)
"""
def indexBIAS(sd, indDay) :
#    print("=== Calculate index BIAS ===")
#    print("the data size is ", len(sd))
    sdEndPrice = list(sd.end_price)
    rtnData = []
    i = 0

    while i < len(sdEndPrice) :
        theBias = 0
        if i < (indDay - 1) :
            theBias = (sdEndPrice[i] - np.mean(sdEndPrice[0:i+1])) / np.mean(sdEndPrice[0:i+1]) * 100
        else :
            theBias = (sdEndPrice[i] - np.mean(sdEndPrice[(i-indDay+1):(i+1)])) / np.mean(sdEndPrice[(i-indDay+1):(i+1)]) * 100
        
        rtnData.append(theBias)
        i += 1
    
    return pd.Series(rtnData, index=sd.trade_date)


"""
說    明: Calculate the Wilder's RSI value
    Formula : WRSI= UP / ( DN+UP) * 100
    WRSI = 100 - (100 / (1 + RS))，其中 RS = UP / DN 
            UP = 期間內絕對漲幅
            DN = 期間內絕對跌幅
輸入參數: 
    sd      股市資料
    indDay  欲計算指標之天數
輸出參數: the WRSI list
版    本: 
    1.00 20130713 新增 (OK)
"""
def indexWRSI(sd, indDay) :
#    print("=== Calculate index WRSI ===")
#    print("the data size is ", len(sd))
    sdEndPrice = list(sd.end_price)
    rtnData = []
    i = 1   # 2nd start
    prevUp = 0
    prevDown = 0
    theWRSI = 50
    rtnData.append(theWRSI)

    while i < len(sdEndPrice) :
        curUp = 0
        curDown = 0
        diffValue = sdEndPrice[i] - sdEndPrice[i-1]
        if diffValue > 0 :
            curUp = diffValue
        else :
            curDown = abs(diffValue)
        
#        print("BEF i=", i, prevUp, curUp, prevDown, curDown)

        if i < (indDay - 1) :
            curUp = (i / (i + 1)) * prevUp + (1 / (i + 1)) * curUp
            curDown = (i / (i + 1)) * prevDown + (1 / (i + 1)) * curDown
        else :
            curUp = (indDay - 1)/indDay * prevUp + (1 / indDay) * curUp
            curDown = (indDay - 1)/indDay * prevDown + (1 / indDay) * curDown

#        print("AFT i=", i, prevUp, curUp, prevDown, curDown)

        if i > 0 and (curUp + curDown) != 0 :
            theWRSI = curUp / (curUp + curDown) *100
        else :
            theWRSI = 50

        rtnData.append(theWRSI)
        prevUp = curUp
        prevDown = curDown
        i += 1
    
    return pd.Series(rtnData, index=sd.trade_date)

