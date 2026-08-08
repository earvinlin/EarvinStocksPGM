#!/bin/bash

#python3 01_getStocksDailyRatiosData_v2.py 20260810 20260814
#python3 02_formatStocksDailyRatiosData_v2.py 20260810 20260814
#python3 03_insertDailyRatiosToMySQLDB_v2.py 20260810 20260814

python3 01_getStocksDailyRatiosData_v2.py 20260803 20260807
python3 02_formatStocksDailyRatiosData_v2.py 20260803 20260807
python3 03_insertDailyRatiosToMySQLDB_v2.py 20260803 20260807
