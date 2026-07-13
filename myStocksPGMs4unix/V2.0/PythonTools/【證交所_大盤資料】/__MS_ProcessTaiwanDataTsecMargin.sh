#!/bin/bash

python MS_getTaiwanDataTsecMarginData_v2.py 202607013 20260717 MS
python MS_formatTaiwanDataTsecMarginData_v2.py 202607013 20260717 MS
python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 202607013 20260717
