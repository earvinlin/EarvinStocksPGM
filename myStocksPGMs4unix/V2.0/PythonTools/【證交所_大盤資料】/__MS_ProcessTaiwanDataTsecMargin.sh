#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20260316 20260320 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20260316 20260320 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260316 20260320
