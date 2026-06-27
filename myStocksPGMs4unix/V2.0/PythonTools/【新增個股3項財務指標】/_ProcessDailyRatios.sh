#!/bin/bash

python3 01_getStocksDailyRatiosData_v2.py 20260522 20260526
python3 02_formatStocksDailyRatiosData_v2.py 20260522 20260526
python3 03_insertDailyRatiosToMySQLDB_v2.py 20260522 20260526
