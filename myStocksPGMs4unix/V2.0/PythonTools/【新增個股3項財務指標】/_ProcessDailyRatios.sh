#!/bin/bash

python3 01_getStocksDailyRatiosData_v2.py 20260511 20260515
python3 02_formatStocksDailyRatiosData_v2.py 20260511 20260515
python3 03_insertDailyRatiosToMySQLDB_v2.py 20260511 20260515
