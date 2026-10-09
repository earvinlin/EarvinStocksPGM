#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20261005 20261008 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20261005 20261008 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20261005 20261008 MS

