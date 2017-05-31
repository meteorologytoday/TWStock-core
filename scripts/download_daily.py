import sys, getopt, os
from datetime import datetime, timedelta
import importlib

db_file = "STOCK.db"
datapath = "."
days=1

doing = []
getting = []

now = datetime.now()
beg_t = now.timestamp()


try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["datapath=", "database=", "TWSE", "TPEX", "stock", "bizcorp", "finmar", "days="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a
	elif o == "--datapath":
		datapath = a
	elif o == "--TWSE":
		doing.append('TWSE')
	elif o == "--TPEX":
		doing.append('TPEX')
	elif o == "--stock":
		getting.append('Stock')
	elif o == "--bizcorp":
		getting.append('BizCorp')
	elif o == "--finmar":
		getting.append('FinMar')
	elif o == "--days":
		days = int(a)

download_beg_t = now - timedelta(days)

print("DATABASE file: %s" % (db_file,))
print("DATABASE path: %s" % (os.path.abspath(datapath),))
print("Doing? %s" % ', '.join(doing))
print("Getting? %s" % ', '.join(getting))

for prefix in doing:
	for data_type in getting:
		
		cls_str = '%sDaily%sDownloader' % (prefix, data_type) 
		cls = getattr(importlib.import_module('TWStock.downloader.%s' % (cls_str,)), cls_str)
		with cls("%s/%s" % (datapath, db_file)) as handler:
			handler.download(download_beg_t, now)

print("下載完成！")
print("共費時%d秒" % (int(datetime.now().timestamp() - beg_t),))
