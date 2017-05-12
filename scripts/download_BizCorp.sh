#/bin/bash
PY=python3

echo "Download Months: $1"

$PY $TWStockPATH/src/download_BizCorp.py --TPEX --TWSE --months=$1 | tee $TWStockPath/log/download_bizcorp.log

echo "Download is finished!"
