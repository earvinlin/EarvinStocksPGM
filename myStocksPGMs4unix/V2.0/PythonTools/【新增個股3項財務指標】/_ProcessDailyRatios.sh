#!/bin/bash

python3 01_getStocksDailyRatiosData_v2.py 20260427 20260430
python3 02_formatStocksDailyRatiosData_v2.py 20260427 20260430
python3 03_insertDailyRatiosToMySQLDB_v2.py 20260427 20260430

# python3 01_getStocksDailyRatiosData_v2.py 20260504 20260508
# python3 02_formatStocksDailyRatiosData_v2.py 20260504 20260508
# python3 03_insertDailyRatiosToMySQLDB_v2.py 20260504 20260508

