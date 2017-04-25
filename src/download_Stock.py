import sys, getopt
import datetime
from TWSEStockDownloader import TWSEStockDownloader
from TPEXStockDownloader import TPEXStockDownloader

now = datetime.date.today()

marker = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
twse_file = 'targets.csv'
tpex_file = 'targets.csv'
db_file = "STOCK.db"
scan = False
targets_dir = 'targets'
months = 12

beg_t = datetime.datetime.now().timestamp()

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database=", "TWSE=", "TPEX=", "scan", "targets-dir=", "marker=", "months="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a
	elif o == "--TWSE":
		twse_file = a
	elif o == "--TPEX":
		tpex_file = a
	elif o == "--targets-dir":
		targets_dir = a
	elif o == "--scan":
		scan = True
	elif o == "--marker":
		marker = a
	elif o == "--months":
		months = int(a)

if scan:
	months = 1

print("DATABASE   file: %s" % (db_file,))
print("TPEX input file: %s" % (tpex_file,))
print("TWSE input file: %s" % (twse_file,))
print("Targets directory: %s" % (targets_dir,))
print("MARKER : %s" % (marker,))

if not scan:
	with TWSEStockDownloader(db_file) as handler:
		handler.download(months=months, targets="%s/%s" % (targets_dir, twse_file))

	with TPEXStockDownloader(db_file) as handler:
		handler.download(months=months, targets="%s/%s" % (targets_dir, tpex_file))
else:
	leftover = None
	with TWSEStockDownloader(db_file) as handler:
		handler.download(months=months, targets="%s/%s" % (targets_dir, twse_file))
		_, leftover = handler.printTargets('TWSE%s' % (marker,), targets_dir=targets_dir)
	with TPEXStockDownloader(db_file) as handler:
		handler.download(months=months, targets=leftover)
		handler.printTargets('TPEX%s' % (marker,), targets_dir=targets_dir)

print("下載完成！")
print("共費時%d秒" % (int(datetime.datetime.now().timestamp() - beg_t),))
