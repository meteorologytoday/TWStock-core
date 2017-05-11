#/bin/bash
set -x
PY=python3

echo "Download Months: $1"

$PY $TWSEStockPATH/src/download_BizCorp.py --TPEX --TWSE --months=$1
# | tee log/download_bizcorp.log

echo "Download is finished!"
