#/bin/bash
scripts_path=$TWStockPATH/scripts
src_path=$TWStockPATH/src
days=$1
if [ -z "$1" ]; then
	days=2
fi

echo "Download Months: $days"
$scripts_path/download_Stock.sh $days
$scripts_path/download_BizCorp.sh $days
python3 $src_path/reorder_data.py --database=STOCK.db
echo "Download is finished!"
