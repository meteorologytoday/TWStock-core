#/bin/bash
scripts_path=$TWSEStockPATH/scripts
src_path=$TWSEStockPATH/src
echo "Download Months: 2"
$scripts_path/download_Stock.sh 12
$scripts_path/download_BizCorp.sh 12
python3 $src_path/reorder_data.py --database=STOCK.db
echo "Download is finished!"
