#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20260522 20260526 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20260522 20260526 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260522 20260526
