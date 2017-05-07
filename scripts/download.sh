#/bin/bash

PY=python3

pid=""

$PY $TWSEStockPATH/src/download_Stock.py --TPEX=TPEX_SCAN_valid_targets.csv --TWSE=TWSE_SCAN_valid_targets.csv --targets-dir=targets --months=24 | tee log_download_stock &
pid="$pid $!"

$PY $TWSEStockPATH/src/download_BizCorp.py --TPEX --TWSE --days=732 | tee log_download_bizcorp &
pid="$pid $!"


echo "Waitng jobs done... pid: $pid"
wait $pid
echo "Download is finished!"
