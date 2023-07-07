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
theIndValues = im.indexKD(theStockData, 5)

#for r in theResult :
#    print(r)
print(len(theIndValues))
print(theIndValues)

