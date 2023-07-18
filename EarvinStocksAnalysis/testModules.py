import os
#from modules.indexes import ind
#import modules.indexes.indexMAP as ind
#from modules.indexes import IndexMAP as ind
from modules.db import stocksData as sd
from modules.indexes import indexesModule as im
from modules.prediction import stocksPrediction as sp

#ind.testMAP("hello modules!")
theStockData = sd.getStocksData("0056")

#theIndValues = ind.indexMAP(theStockData, 5)
#theIndValues = im.indexMAP(theStockData, 5)
# index VR verify OK (20230707)
#theIndValues = im.indexVR(theStockData, 5)

# index KD 
"""
theIndValues = im.indexKD(theStockData, 9)
theTradeDate = theIndValues["TradeDate"]
theK = theIndValues["K"]
theD = theIndValues["D"]
theRSV = theIndValues["RSV"]
"""

# index BIAS
#theIndValues = im.indexBIAS(theStockData, 10)

# index WRSI
#theIndValues = im.indexWRSI(theStockData[0:15], 5)
#theIndValues = im.indexWRSI(theStockData, 14)


#for r in theResult :
#    print(r)
#print(len(theIndValues))
#print(theIndValues[3791:3795])
#print(theIndValues)

"""
print(theTradeDate[3791:3795])
print(theK[3791:3795])
print(theD[3791:3795])
print(theRSV[3791:3795])
"""


# TestCase : test splitSector() 
"""
theCompV1 = im.indexMAP(theStockData, 20)
theCompV2 = im.indexMAP(theStockData, 60)
print(theCompV1)
print(theCompV2)
theSectors = sp.splitSector(theCompV1, theCompV2)
print(theSectors)
"""

# TestCase : test preProcess()
theCompV1 = im.indexMAP(theStockData, 20)
theCompV2 = im.indexMAP(theStockData, 60)
theSectors = sp.splitSector(theCompV1, theCompV2)
print(theSectors)

preValue = theSectors.iloc[0]  
print(preValue)

i = 1
lastLoc = 0
while  i < len(theSectors) :
    if preValue == theSectors.iloc[i] :
        i += 1
    else : 
        lastLoc = i
        break
#sss = theSectors[0:lastLoc]
theIndValues = im.indexBIAS(theStockData, 10)
print(theIndValues[0:lastLoc])
thePreProcessData = sp.preProcess(theIndValues[0:lastLoc], sp.CLS_MAX)
print(thePreProcessData)


