import sys, getopt
import datetime
from TWSEBizCorpDownloader import TWSEBizCorpDownloader
from TPEXBizCorpDownloader import TPEXBizCorpDownloader
import TimeFuncs

beg_t = datetime.datetime.now().timestamp()

db_file = "STOCK.db"
twse = False
tpex = False
months = 1


try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database=", "TWSE", "TPEX", "months="])
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
	elif o == "--months":
		months = int(a)


now = datetime.datetime.utcnow()
y, m = TimeFuncs.prevMonth(now.year, now.month, months)
before = datetime.datetime(y, m, 1, tzinfo=datetime.timezone.utc)
days = int(float(now.timestamp() - before.timestamp()) / 86400.0 + 1)


print("資料庫檔案：%s" % (db_file,))
print("追溯時間： %d 日 (從%s到%s)" % (days,before.strftime("%Y/%m/%d"), now.strftime("%Y/%m/%d")))
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
