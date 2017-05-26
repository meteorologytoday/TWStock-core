#/bin/bash
PY=python3

echo "Download days: $1"

$PY $TWStockPATH/src/download_DailyBizCorp.py --TPEX --TWSE --days=$1 | tee $TWStockPath/log/download_bizcorp.log

echo "Download is finished!"
