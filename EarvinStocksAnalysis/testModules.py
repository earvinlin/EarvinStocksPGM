import os
#from modules.indexes import ind
#import modules.indexes.indexMAP as ind
#from modules.indexes import IndexMAP as ind
from modules.db import stocksData as sd
from modules.indexes import indexesModule as im

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
theIndValues = im.indexBIAS(theStockData, 10)

#for r in theResult :
#    print(r)
print(len(theIndValues))
print(theIndValues[3791:3795])
"""
print(theTradeDate[3791:3795])
print(theK[3791:3795])
print(theD[3791:3795])
print(theRSV[3791:3795])
"""
