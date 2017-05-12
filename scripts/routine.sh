#/bin/bash
scripts_path=$TWSEStockPATH/scripts
src_path=$TWSEStockPATH/src
months=$1
if [ -z "$1" ]; then
	months=2
fi

echo "Download Months: $months"
$scripts_path/download_Stock.sh $months
$scripts_path/download_BizCorp.sh $months
python3 $src_path/reorder_data.py --database=STOCK.db
echo "Download is finished!"
