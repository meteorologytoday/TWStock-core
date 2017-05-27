from StockIO import StockDownloader
import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout
from StockShare import *
import TimeFuncs

HOST = "http://www.tpex.org.tw"
cvs_data_cols = ['no', 'stockname', 'c_p', 'change_spread', 'o_p', 'h_p', 'l_p', 'vol', 'turnover', 'count']
float_data = ['vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

def fetch_data(req_time):
	params = {
		'l'  : 'zh-tw',
		'd'  : "%d/%02d/%02d" % (req_time.year - 1911, req_time.month, req_time.day),
		'se' : 'AL',
		's'  : '0,asc,0'
	}
	params = urllib.parse.urlencode(params)
	req = urllib.request.Request(
		HOST + '/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_download.php?' + params
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
missing_data_filter = re.compile(r'^-{2,}$')
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
				
			fixed = False
			# 該日無漲跌
			if missing_data_filter.match(row['o_p']):
				fixed = True
	
			row['change_spread'] = row['change_spread'].replace('X', '')

			ex_div_right = False
			if row['change_spread'] in ['除息', '除權']:
				row['change_spread'] = '0'
				ex_div_right = True

			if fixed:
				for key in float_data:
					row[key] = None
			else:
				for key in float_data:
					row[key] = float(row[key].replace(',', ''))

			if ex_div_right:
				row['change_spread'] = row['c_p'] - row['o_p']

			data.append(row)

	return data


class TPEXDailyStockDownloader(StockDownloader):
	def __init__(self, db_fname):
		super().__init__(db_fname)


	def download(self, beg_date=datetime.datetime.now(), end_date=datetime.datetime.now()):

		print("收集TPEX資料，時間 %s 至 %s" % (beg_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d")))
		# iterate over time
		for today in TimeFuncs.iter_date(beg_date, end_date, include_end=True):
			print("收集TPEX資料: %s" % today.strftime("%Y/%m/%d"))
				
			err = []

			try:
				retrieved = fetch_data(today)
			except Exception as e:
				print("錯誤發生，跳過！")
				print(str(e))
				err.append([today.strftime('%Y/%m/%d'), 'fetch_data:' + str(e)])
				continue


			try:
				data = parseFile(retrieved)
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)
				print("解析CSV錯誤發生，跳過！")
				print(str(e))
				err.append([req_time.strftime('%Y/%m/%d'), 'fetch_data:' + str(e)])
				continue

			for i in range(len(data)):
				data[i]['date'] = today.timestamp() 

			print("[%s] 寫入資料庫(共%d筆)" % (today.strftime('%Y/%m/%d'), len(data)))
			self.writeDB(data)
			sys.stdout.flush()
