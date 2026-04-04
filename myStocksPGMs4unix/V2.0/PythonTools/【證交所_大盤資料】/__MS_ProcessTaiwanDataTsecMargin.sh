#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20260406 20260410 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20260406 20260410 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260406 20260410
