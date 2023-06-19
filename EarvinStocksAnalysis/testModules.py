import os
#from modules.indexes import ind
#import modules.indexes.indexMAP as ind
from modules.indexes import IndexMAP as ind
from modules.db import StocksData as sd

ind.testMAP("hello modules!")
theResult = sd.GetStocksData("0056")
for r in theResult :
    print(r)
print(len(theResult))
