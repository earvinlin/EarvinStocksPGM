#!/bin/bash

#python3 01_getStocksDailyRatiosData_v2.py 20260921 20260924
#python3 02_formatStocksDailyRatiosData_v2.py 20260921 20260924
#python3 03_insertDailyRatiosToMySQLDB_v2.py 20260921 20260924

python3 01_getStocksDailyRatiosData_v2.py 20250920 20260920
python3 02_formatStocksDailyRatiosData_v2.py 20250920 20260920
python3 03_insertDailyRatiosToMySQLDB_v2.py 20250920 20260920
