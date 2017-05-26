import sys, getopt
from datetime import datetime, timedelta
from Downloader.TWSEDailyStockDownloader import TWSEDailyStockDownloader

db_file = "STOCK.db"
days=1
do_twse = False
do_tpex = False

now = datetime.now()

beg_t = now.timestamp()
download_beg_t = now - timedelta(days)

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database=", "TWSE", "TPEX", "months="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a
	elif o == "--TWSE":
		do_twse = True
	elif o == "--TPEX":
		do_tpex = True
	elif o == "--months":
		months = int(a)

print("DATABASE   file: %s" % (db_file,))
print("Doing TWSE? %s" % ("Yes" if do_twse else "No",))
print("Doing TPEX? %s" % ("Yes" if do_tpex else "No",))

with TWSEDailyStockDownloader(db_file) as handler:
		handler.download(download_beg_t, now)


print("下載完成！")
print("共費時%d秒" % (int(datetime.now().timestamp() - beg_t),))
