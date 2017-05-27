#/bin/bash

PY=python3

echo "Download days: $1"

$PY $TWStockPATH/src/download_DailyStock.py --TPEX --TWSE --days=$1 | tee $TWStockPATH/log/download_stock.log

echo "Download is finished!"
