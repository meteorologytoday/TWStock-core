#!/bin/bash

stored=$TWStockPATH/web/data

python3 $TWStockPATH/tools/01.py > $stored/`date +%Y%m%d`
