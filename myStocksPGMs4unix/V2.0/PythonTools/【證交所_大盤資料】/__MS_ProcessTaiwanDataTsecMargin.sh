#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20260622 20260626 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20260622 20260626 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260622 20260626
