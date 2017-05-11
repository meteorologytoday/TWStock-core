from StockIO import StockDownloader
import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout
from StockShare import *
import TimeFuncs

TWSE_HOST = "http://www.twse.com.tw/"
cvs_data_cols = ['date', 'vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

strip = ['vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

def stripcma(s):
	return s.replace(',', '')


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


class TWSEStockDownloader(StockDownloader):
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
			y, m = TimeFuncs.prevMonth(now.year, now.month, i)
			req_times.append(datetime.datetime(y, m, 1, tzinfo=datetime.timezone.utc))

		
		with open(kwargs['targets'], 'r') as target_file:
			for stock in csv.DictReader(target_file, ['stockno', 'name']):

				name = stock['name']
				stockno = stock['stockno']
				data = []
				err = []
				for req_time in req_times:
					print("收集TWSE[%s]資料(編號%s), %04d年%02d月" % (name, stockno, req_time.year, req_time.month))

					retrieved = fetch_data(stockno, req_time)
					if retrieved is None:
						print("錯誤發生，跳過！")
						err.append('fetch_data')
						continue

					with StringIO(fetch_data(stockno, req_time)) as pseudofile:
						stock_reader = csv.DictReader(
							pseudofile,
							cvs_data_cols
						)
						
						stock_name = 'Unknown'
						try:
							stock_name = next(stock_reader)['date'].split()[1]
							next(stock_reader)
						except StopIteration:
							print("讀取CSV時錯誤發生，跳過！")
							err.append('csv')
							continue
							

						for row in stock_reader:
							if row['date'] == '查無資料！' or row['date'] is None:
								print("查無資料，跳過！")
								err.append('empty')
								break
		
							fixed = False
							# 該日無漲跌
							if row['o_p'] == '0.00':
								print("%s 無價格波動！" % (row['date'],))
								fixed = True

							tmp = row['date'][0:9].split('/')
							row['date'] = int(datetime.datetime(int(tmp[0])+1911, int(tmp[1]), int(tmp[2]), tzinfo=datetime.timezone.utc).timestamp())

							row['no'] = stockno	
							row['change_spread'] = row['change_spread'].replace('X', '')
							
							if fixed:
								for key in strip:
									row[key] = None
							else:
								for key in strip:
									row[key] = float(stripcma(row[key]))



							data.append(row)

				if len(err) == 0:
					print(stock_name)
					self.addValidTarget(stockno, stock_name)
				else:
					self.addErrorTarget(stockno, ';'.join(err))

				self.writeDB(data)
				sys.stdout.flush()
