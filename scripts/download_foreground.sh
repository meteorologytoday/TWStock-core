#/bin/bash

PY=python3

$PY $TWSEStockPATH/src/download_Stock.py --TPEX=TPEX_SCAN_valid_targets.csv --TWSE=TWSE_SCAN_valid_targets.csv --targets-dir=targets --months=2

$PY $TWSEStockPATH/src/download_BizCorp.py --TPEX --TWSE --days=60

echo "Download is finished!"
