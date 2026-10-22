#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 20261019 20261022 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 20261019 20261022 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20261019 20261022 MS

