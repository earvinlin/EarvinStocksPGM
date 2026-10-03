#!/bin/bash

python3 03_getTaiwanDataTsecVolumeData.py 20260901
python3 03_formatTaiwanDataTsecVolumeData.py 20260901

python3 03_getTaiwanDataTsecVolumeData.py 20261001
python3 03_formatTaiwanDataTsecVolumeData.py 20261001
