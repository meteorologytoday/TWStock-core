from TWStock.core.BizCorpIO import BizCorpDownloader
import TWStock.core.TimeFuncs as TimeFuncs

import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout

HOST = "http://www.tpex.org.tw"

# 民國103年12/01開始自營商欄位區分成避險買賣等等
# 目前設計僅針對103年12/01之後的表格(這個部分處理極為痛苦)

cvs_data_cols = [                                         \
	'no', 'name',                                         \
	'foreign_i', 'foreign_o', 'foreign_n',                \
	'trust_i', 'trust_o', 'trust_n',                      \
	'dealer_net',                                         \
	'dealer_self_i', 'dealer_self_o', 'dealer_self_n',    \
	'dealer_hedge_i', 'dealer_hedge_o', 'dealer_hedge_n', \
	'net'
]

float_data = ['foreign_i', 'foreign_o', 'trust_i', 'trust_o', 'dealer_self_i', 'dealer_self_o', 'dealer_hedge_i', 'dealer_hedge_o']



def fetch_data(req_time):
	params = {
		'l'  : 'zh-tw',
		't'   : 'D',
		'd'   : "%d/%02d/%02d" % (req_time.year-1911, req_time.month, req_time.day),
		'se'  : 'AL',
		's'   : '0,asc'
	}
	params = urllib.parse.urlencode(params)
	req = urllib.request.Request(
		HOST + '/web/stock/3insti/daily_trade/3itrade_hedge_download.php?' + params
	)

	try:
		with urllib.request.urlopen(req, timeout=10) as response:
			data = response.read()
			data = data.decode('cp950')
	except urllib.error.URLError as e:
		raise Exception("URL 錯誤")
	except timeout as e:
		raise Exception("長時間無回應")
	
	return data

#stockno_filter = re.compile(r'^[\dA-Z]+$')
stockno_filter = re.compile(r'^\d{4}$')
char_filter = re.compile(r'[ =]')
def parseFile(text):
	global stockno_filter, char_filter
	text = char_filter.sub('', text)
	data = []
	if len(text) == 0:
		return data

	with StringIO(text) as pseudofile:
		stock_reader = csv.DictReader(
			pseudofile,
			cvs_data_cols
		)
		
		for row in stock_reader:
			# 判定此列為資料列
			if not stockno_filter.match(row['no']):
				continue
			
			for key in float_data:
				row[key] = float(row[key].replace(',', ''))
	
			data.append(row)

	return data


class TPEXDailyBizCorpDownloader(BizCorpDownloader):
	def __init__(self, db_fname):
		super().__init__(db_fname)


	def download(self, beg_date=datetime.datetime.now(), end_date=datetime.datetime.now()):

		print("收集TPEX三大法人資料，時間 %s 至 %s" % (beg_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d")))
		# iterate over time
		for today in TimeFuncs.iter_date(beg_date, end_date, include_end=True):
			print("收集TPEX三大法人資料: %s" % today.strftime("%Y/%m/%d"))
				
			err = []
			retrieved = fetch_data(today)
			try:
				pass
			except Exception as e:
				print("錯誤發生，跳過！")
				print(str(e))
				err.append([today.strftime('%Y/%m/%d'), 'fetch_data:' + str(e)])
				continue


			data = parseFile(retrieved)
			try:
				pass
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)
				print("解析CSV錯誤發生，跳過！")
				print(str(e))
				err.append([today.strftime('%Y/%m/%d'), 'fetch_data:' + str(e)])
				continue

			for i in range(len(data)):
				data[i]['date'] = today.timestamp() 

			print("[%s] 寫入資料庫(共%d筆)" % (today.strftime('%Y/%m/%d'), len(data)))
			self.writeDB(data)
			sys.stdout.flush()
