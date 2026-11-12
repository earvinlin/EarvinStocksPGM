#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20261102 20261106 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20261102 20261106 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20261102 20261106 MS


