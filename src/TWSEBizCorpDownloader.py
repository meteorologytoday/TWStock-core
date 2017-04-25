import BizCorpShare
from BizCorpIO import BizCorpDownloader
import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
from socket import timeout

TWSE_HOST = "http://www.twse.com.tw/"



cvs_data_cols = [                                         \
	'no', 'name',                                         \
	'foreign_i', 'foreign_o', 'foreign_n',                \
	'trust_i', 'trust_o', 'trust_n',                      \
	'dealer_net',                                         \
	'dealer_self_i', 'dealer_self_o', 'dealer_self_n',    \
	'dealer_hedge_i', 'dealer_hedge_o', 'dealer_hedge_n', \
	'net'
]

strip = ['foreign_i', 'foreign_o', 'trust_i', 'trust_o', 'dealer_self_i', 'dealer_self_o', 'dealer_hedge_i', 'dealer_hedge_o']


def stripcma(s):
	return s.replace(',', '')

def fetch_data(req_time):
	params = {
		'download'    : 'csv',
		'qdate'       : "%03d/%02d/%02d" % (req_time.year - 1911, req_time.month, req_time.day),
		'select2'     : 'ALLBUT0999', # 全部(不含權證、牛熊證、可展延牛熊證)
		'sorting'     : 'by_stkno'
	}
	data = urllib.parse.urlencode(params)
	data = data.encode('ascii') # data should be bytes
	req = urllib.request.Request(
		TWSE_HOST + 'ch/trading/fund/T86/T86.php',
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


class TWSEBizCorpDownloader(BizCorpDownloader):
	def __init__(self, db_fname):
		super().__init__(db_fname)

	def download(self, **kwargs):

		if kwargs.get('days') is None:
			kwargs['days'] = 60

		today = int(datetime.datetime.utcnow().timestamp() / 86400.0 ) * 86400
		req_times = [today - 86400*i for i in range(0, kwargs['days'])]
		
		for req_time in req_times:
			data = []
			err = []

			timestamp = req_time
			req_time = datetime.datetime.fromtimestamp(req_time, tz=datetime.timezone.utc)

			print("收集TWSE%04d年%02d月%02d日三大法人資料" % (req_time.year, req_time.month, req_time.day))
			retrieved = fetch_data(req_time)
			if retrieved is None:
				print("錯誤發生，跳過！")
				err.append('fetch_data')
				continue

			with StringIO(fetch_data(req_time)) as pseudofile:
				reader = csv.DictReader(
					pseudofile,
					cvs_data_cols
				)
				
				stock_name = 'Unknown'
				try:
					next(reader)
					next(reader)
				except StopIteration:
					print("讀取CSV時錯誤發生，跳過！")
					err.append('csv')
					continue
			

				for row in reader:
					row['date'] = timestamp		
					if row['name'] is None:
						break

					for key in strip:
						row[key] = float(stripcma(row[key]))

					row['no'] = row['no'][2:-1].strip()
					data.append(row)
					
				if len(err) != 0:
					self.addError(req_time.strftim("%Y-%m-%d"), ';'.join(err))

			self.writeDB(data)
