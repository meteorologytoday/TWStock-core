import sys, getopt
from datetime import datetime, timedelta


db_file = "STOCK.db"
days=1
do_twse = False
do_tpex = False

now = datetime.now()
beg_t = now.timestamp()


try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database=", "TWSE", "TPEX", "days="])
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
	elif o == "--days":
		days = int(a)

download_beg_t = now - timedelta(days)

print("DATABASE   file: %s" % (db_file,))
print("Doing TWSE? %s" % ("Yes" if do_twse else "No",))
print("Doing TPEX? %s" % ("Yes" if do_tpex else "No",))

if do_twse:
	from Downloader.TWSEDailyStockDownloader import TWSEDailyStockDownloader
	with TWSEDailyStockDownloader(db_file) as handler:
		handler.download(download_beg_t, now)

if do_tpex:
	from Downloader.TPEXDailyStockDownloader import TPEXDailyStockDownloader
	with TPEXDailyStockDownloader(db_file) as handler:
		handler.download(download_beg_t, now)


print("下載完成！")
print("共費時%d秒" % (int(datetime.now().timestamp() - beg_t),))
