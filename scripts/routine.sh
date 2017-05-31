#/bin/bash
days=$1
if [ -z "$1" ]; then
	days=1
fi

datapath=$2
if [ -z "$2" ]; then
	datapath='.'
fi

d=`dirname $0`

echo "Download Months: $days"
python3 $d/download_daily.py --TPEX --TWSE --stock --bizcorp --finmar --days=$days --datapath=$datapath
python3 $d/reorder_data.py --datapath=$datapath
echo "Download is finished!"
