import pandas as pd
import numpy as np
from modules.indexes import IndexMAP as ind
from modules.db import StocksData as sd

ind.testMAP("hello modules!")

theStocksData = sd.GetStocksData("0056")

#theStocksData.to_csv("0056.csv")
#theResult = ind.testMAP2("0056")
#for r in theResult :
#    print(r)
#print(len(theResult))
#print(theResult)

theValue = ind.indexMAP(theStocksData, 10)
print("== The result is ==")
print(theValue)

