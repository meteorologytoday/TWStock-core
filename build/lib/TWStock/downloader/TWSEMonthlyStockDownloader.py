from StockIO import StockDownloader
import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout
from StockShare import *
import TimeFuncs

TWSE_HOST = "http://www.twse.com.tw"
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
		'response'    : 'csv',
		'date'        : req_time.strftime("%Y%m%d"),
		'stockNo'     : stockno
	}



	params = urllib.parse.urlencode(params)
	req = urllib.request.Request(
		TWSE_HOST + '/exchangeReport/STOCK_DAY?' + params
	)

	try:
		with urllib.request.urlopen(req, timeout=1) as response:
			data = response.read()
			data = data.decode('cp950')
			print(data)
	except urllib.error.URLError as e:
		raise Exception("URL 錯誤")
	except timeout as e:
		raise Exception("長時間無回應")
	
	return data

date_matcher = re.compile(r'^\d+/\d{2}/\d{2}$') 
def parseFile(stockno, text):
	global date_matcher
	text = text.replace('=', '')
	data = []
	with StringIO(text) as pseudofile:
		stock_reader = csv.DictReader(
			pseudofile,
			cvs_data_cols
		)
		
		stock_name = 'Unknown'
		try:
			stock_name = next(stock_reader)['date'].split()[2]
			next(stock_reader)
		except StopIteration:
			print("讀取CSV時錯誤發生，跳過！")
			raise Exception('csv')
			
		for row in stock_reader:
			if row['date'] == '查無資料！':
				print("查無資料，跳過！")
				raise Exception('Empty data')
				break

			if not date_matcher.match(row['date']):
				continue
				
			fixed = False
			# 該日無漲跌
			if row['o_p'] == '--':
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

	return data, stock_name


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

					try:
						retrieved = fetch_data(stockno, req_time)
					except Exception as e:
						print("錯誤發生，跳過！")
						err.append('fetch_data:' + str(e))
						continue
					new_data, stock_name = parseFile(stockno, retrieved)
					data.extend(new_data)
					try:
						pass
					except Exception as e:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
						print(exc_type, fname, exc_tb.tb_lineno)
						print("解析CSV錯誤發生，跳過！")
						print(str(e))
						err.append('fetch_data:' + str(e))
						continue
					 
				if len(err) == 0:
					print(stock_name)
					self.addValidTarget(stockno, stock_name)
				else:
					self.addErrorTarget(stockno, ';'.join(err))

				self.writeDB(data)
				sys.stdout.flush()
