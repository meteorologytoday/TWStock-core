#/bin/bash
scripts_path=$TWStockPATH/scripts
src_path=$TWStockPATH/src
days=$1
if [ -z "$1" ]; then
	days=1
fi

echo "Download Months: $days"
python3 $src_path/download_daily.py --TPEX --TWSE --stock --bizcorp --finmar --days=$days --datapath=$TWStockDataPATH
python3 $src_path/reorder_data.py --datapath=$TWStockDataPATH
echo "Download is finished!"
