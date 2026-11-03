#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20261027 20261030 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20261027 20261030 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20261027 20261030 MS

