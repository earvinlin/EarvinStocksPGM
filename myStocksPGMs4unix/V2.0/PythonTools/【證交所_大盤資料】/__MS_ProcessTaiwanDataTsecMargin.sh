#!/bin/bash

#python MS_getTaiwanDataTsecMarginData_v2.py 20260810 20260814 MS
#python MS_formatTaiwanDataTsecMarginData_v2.py 20260810 20260814 MS
#python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260810 20260814

python MS_getTaiwanDataTsecMarginData_v2.py 20260803 20260807 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20260803 20260807 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260803 20260807
