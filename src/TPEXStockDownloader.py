from StockIO import StockDownloader
import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout
import time
HOST = "http://www.tpex.org.tw/"
cvs_data_cols = ['date', 'vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

strip = ['vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

def stripcma(s):
	return s.replace(',', '')


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
		'l'     : 'zh-tw',
		'd'     : "%d/%02d" % (req_time.year-1911, req_time.month),
		'stkno' : stockno
	}

	req = urllib.request.Request(
		HOST + 'web/stock/aftertrading/daily_trading_info/st43_download.php?' + urllib.parse.urlencode(params)
	)
	

	try:
		with urllib.request.urlopen(req, timeout=1) as response:
			if response.info().get('Content-Type') == 'application/csv':
				data = response.read().decode('cp950', 'ignore')
			else:
				data = None
				print("Wrong Content-type:" + response.info().get('Content-Type'))
	except urllib.error.URLError:
		data = None 
	except timeout:
		data = None
		
	return data


class TPEXStockDownloader(StockDownloader):
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
#			i = 11 - i
			y, m = prevMonth(now.year, now.month, i)
			req_times.append(datetime.datetime(y, m, 1, tzinfo=datetime.timezone.utc))

		
		with open(kwargs['targets'], 'r') as target_file:
			for stock in csv.DictReader(target_file, ['stockno', 'name']):
				name = stock['name']
				stockno = stock['stockno']
				data = []
				err = []
				for req_time in req_times:
					print("收集股市資料(編號%s), %04d年%02d月" % (stockno, req_time.year, req_time.month))

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
							next(stock_reader)
							next(stock_reader)
							stock_name = next(stock_reader)['date'].split(':')[1]
							next(stock_reader)
							next(stock_reader)
						except StopIteration:
							print("讀取CSV時錯誤發生，跳過！")
							err.append('csv')
							continue
						for row in stock_reader:
							if row['date'][0:3] == '共0筆':
								print("查無資料，跳過！")
								err.append('empty')
								break
							elif row['date'][0] == '共':
								break

							# 不明原因沒有開盤價，跳過這筆
							if row['o_p'] == '--':
								print("%s 資料有異開盤內容為'%s'，跳過！" % (row['date'],row['o_p']))
								continue							

							tmp = row['date'][0:9].split('/')
							row['date'] = int(datetime.datetime(int(tmp[0])+1911, int(tmp[1]), int(tmp[2]), tzinfo=datetime.timezone.utc).timestamp())
							row['no'] = stockno
			
							row['change_spread'] = row['change_spread'].replace('X', '')
							for key in strip:
								row[key] = float(stripcma(row[key]))
							

							data.append(row)

				if len(err) == 0:
					print(stock_name)
					self.addValidTarget(stockno, stock_name) 
				else:
					self.addErrorTarget(stockno, ';'.join(err))

				self.writeDB(data)
