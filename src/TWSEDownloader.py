from Stock import StockDownloader
import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout

TWSE_HOST = "http://www.twse.com.tw/"
cvs_data_cols = ['date', 'vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

def prevMonth(year, month, dmonth):
	"""
		One base: 1 = Jan, 2 = Feb, ..., 12 = Dec.
	"""
	time = year + (month - 1 - dmonth) / 12.0
	return int(round(time)), int(round((time - int(time)) * 12.0 + 1))

def fetch_data(stockno, req_time):
	"""
		0. 日期
		1. 成交股數
		2. 成交金額
		3. 開盤價
		4. 最高價
		5. 最低價
		6. 收盤價
		7. 漲跌價差
		8. 成交筆數
	"""
	params = {
		'download'    : 'csv',
		'query_year'  : str(req_time.year),
		'query_month' : str(req_time.month),
		'CO_ID'       : stockno
	}
	data = urllib.parse.urlencode(params)
	data = data.encode('ascii') # data should be bytes
	req = urllib.request.Request(
		TWSE_HOST + 'ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php',
		data
	)

	try:
		with urllib.request.urlopen(req, timeout=1) as response:
			data = response.read().decode('cp950')
	except urllib.error.URLError:
		data = None 
	except timeout:
		data = None
		

	
	return data


class TWSEDownloader(StockDownloader):
	def __init__(self, db_fname):
		super().__init__(db_fname)

	def download(self, **kwargs):

		if kwargs.get('months') is None:
			kwargs['months'] = 12

		if kwargs.get('targets') is None:
			raise TypeError('Need supplement "targets" keyword arg.')

		now = datetime.date.today()
		req_times = []
		
		for i in range(0, kwargs['months']):
			i = 11 - i
			y, m = prevMonth(now.year, now.month, i)
			req_times.append(datetime.datetime(y, m, 1))

		
		with open(kwargs['targets'], 'r') as target_file:
			for stock in csv.DictReader(target_file, ['stockno', 'name']):
				name = stock['name']
				stockno = stock['stockno']
				data = []
				for req_time in req_times:
					print("收集股市資料(編號%s), %04d年%02d月" % (stockno, req_time.year, req_time.month))

					retrieved = fetch_data(stockno, req_time)
					if retrieved is None:
						print("錯誤發生，跳過！")
						continue

					with StringIO(fetch_data(stockno, req_time)) as pseudofile:
						stock_reader = csv.DictReader(
							pseudofile,
							cvs_data_cols
						)

						try:
							next(stock_reader)
							next(stock_reader)
						except StopIteration:
							print("讀取CSV時錯誤發生，跳過！")
							continue
							

						for row in stock_reader:
							if row['date'] == '查無資料！' or row['date'] is None:
								print("查無資料，跳過！")
								break
	
							tmp = row['date'].split('/')
							row['date'] = "%04d-%02d-%02d" % (int(tmp[0])+1911, int(tmp[1]), int(tmp[2]))

							row['no'] = stockno
							row['vol'] = row['vol'].replace(',','')
							row['turnover'] = row['turnover'].replace(',','') 	
							row['count'] = row['count'].replace(',','') 	
							data.append(row)
				print("** 寫入資料庫")
				self.writeDB(data)
