#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20260525 20260529 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20260525 20260529 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260525 20260529
