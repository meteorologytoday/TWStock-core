#/bin/bash
scripts_path=$TWStockPATH/scripts
src_path=$TWStockPATH/src
web_path=$TWStockPATH/web
months=$1
if [ -z "$1" ]; then
	months=2
fi

set -x

download_status_file=$web_path/status/downloading

echo "Download Months: $months"
echo '{"status":"busy"}' > $download_status_file 
$scripts_path/download_Stock.sh $months
$scripts_path/download_BizCorp.sh $months
python3 $src_path/reorder_data.py --database=STOCK.db
echo "Download is finished!"
rm $download_status_file
