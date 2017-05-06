#/bin/bash

PY=python3

$PY $TWSEStockPATH/src/download_Stock.py --TPEX=TPEX_SCAN_valid_targets.csv --TWSE=TWSE_SCAN_valid_targets.csv --targets-dir=targets --months=24

$PY $TWSEStockPATH/src/download_BizCorp.py --TPEX --TWSE --days=732

echo "Download is finished!"
