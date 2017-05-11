#/bin/bash

PY=python3

echo "Download Months: $1"

$PY $TWSEStockPATH/src/download_Stock.py --TPEX=TPEX_SCAN_valid_targets.csv --TWSE=TWSE_SCAN_valid_targets.csv --targets-dir=targets --months=$1 | tee log/download_stock.log

echo "Download is finished!"