import pandas as pd
import numpy as np

# 20230625 如何用把自己寫的模組使用上面的指令匯入
from modules.indexes import IndexMAP as ind
from modules.indexes import IndexMAV as imav
from modules.indexes import IndexBIAS as ibais
#import modules.indexes.* -- cannot use

from modules.db import StocksData as sd

#ind.testMAP("hello modules!")

theStocksData = sd.GetStocksData("0056")

#theStocksData.to_csv("0056.csv")
#theResult = ind.testMAP2("0056")
#for r in theResult :
#    print(r)
#print(len(theResult))
#print(theResult)

#theValue = ind.indexMAP(theStocksData, 10)
#theValue = imav.indexMAV(theStocksData, 10)
theValue = ibais.indexBIAS(theStocksData, 10)

# 將資料寫入stocksData
#theStocksData['indMAV10'] = theValue
theStocksData['indBIAS10'] = theValue

print("== The result is ==")
print(theStocksData)

