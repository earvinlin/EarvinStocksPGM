#!/bin/bash

sh __GetTaiwanDataTsec.sh  
sh __InsertTaiwanDataTsec.sh
    
sh __GetTaiwanDataTsecVolume.sh
sh __InsertTaiwanDataTsecVolume.sh

sh __MS_ProcessTaiwanDataTsecMargin.sh