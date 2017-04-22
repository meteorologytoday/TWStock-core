import sys, getopt
import datetime
from TWSEBizCorpDownloader import TWSEBizCorpDownloader
from TPEXBizCorpDownloader import TPEXBizCorpDownloader


beg_t = datetime.datetime.now().timestamp()

db_file = "STOCK.db"
twse = False
tpex = False
days = 10


try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database=", "TWSE", "TPEX", "days="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a
	elif o == "--TWSE":
		twse = True
	elif o == "--TPEX":
		tpex = True
	elif o == "--days":
		days = int(a)



print("資料庫檔案：%s" % (db_file,))
print("追溯時間： %d 日" % (days,))
print("下載TPEX？ %s" % ('是' if tpex else '否',))
print("下載TWSE？ %s" % ('是' if twse else '否',))


if twse:
	with TWSEBizCorpDownloader(db_file) as handler:
		handler.download(days=days)

if tpex:
	with TPEXBizCorpDownloader(db_file) as handler:
		handler.download(days=days)

end_t = datetime.datetime.now().timestamp()
print("下載完成！")
print("花費時間：%.1f 分鐘" % (float(end_t - beg_t) / 60.0,))
