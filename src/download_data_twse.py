import urllib.parse
import urllib.request
import json, re, sys, os, csv
from io import StringIO
import datetime
import sqlite3

TWSE_HOST = "http://www.twse.com.tw/"
data_dir = "data_twse"
os.mkdir(data_dir) if not os.path.exists(data_dir) else None

db_file = "test.db"

print("Going to read %s" % (sys.argv[1],))


def prevMonth(year, month, dmonth):
	"""
		One base: 1 = Jan, 2 = Feb, ..., 12 = Dec.
	"""
	time = year + (month - 1 - dmonth) / 12.0
	return int(round(time)), int(round((time - int(time)) * 12.0 + 1))
	

# collect past 12 months data
req_times = []
now = datetime.date.today()
for i in range(0, 12):
	i = 11 - i
	y, m = prevMonth(now.year, now.month, i)
	req_times.append(datetime.datetime(y, m, 1))

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
		'CO_ID'       : stock['stockno']
	}
	data = urllib.parse.urlencode(params)
	data = data.encode('ascii') # data should be bytes
	req = urllib.request.Request(
		TWSE_HOST + 'ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php',
		data
	)
	with urllib.request.urlopen(req) as response:
		data = response.read().decode('cp950')

	
	return data

def createDB(fname):
	c = sqlite3.connect(fname)
	c.execute('''CREATE TABLE IF NOT EXISTS stocks (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		no TEXT,
		date TEXT,
		vol INTEGER,
		turnover INTEGER,
		o_p REAL,
		h_p REAL,
		l_p REAL,
		c_p REAL,
		change_spread REAL,
		count INTEGER,
		UNIQUE(date, no)
	)''')
	c.commit()
	return c



db_conn = createDB(db_file)

cvs_data_cols = ['date', 'vol', 'turnover', 'o_p', 'h_p', 'l_p', 'c_p', 'change_spread', 'count']

db_data_cols = cvs_data_cols.copy()
db_data_cols.insert(0, 'no')
ins_cmd = 'INSERT OR IGNORE INTO stocks(' + ','.join(db_data_cols)+ ') VALUES (:' + ',:'.join(db_data_cols) + ')'

with open(sys.argv[1], 'r') as target_file:
	for stock in csv.DictReader(target_file, ['stockno', 'name']):
		name = stock['name']
		stockno = stock['stockno']


		stock_dir =  "%s/%s" % (data_dir, stockno)
		os.mkdir(stock_dir) if not os.path.exists(stock_dir) else None
	
		for req_time in req_times:
			print("收集股市資料(編號%s), %04d年%02d月" % (stockno, req_time.year, req_time.month), end="\r")
			
			with StringIO(fetch_data(stockno, req_time)) as pseudofile:
				stock_reader = csv.DictReader(
					pseudofile,
					cvs_data_cols
				)
				next(stock_reader)
				next(stock_reader)

				for row in stock_reader:
					print(row)
					if row['date'] == '查無資料！' or row['date'] is None:
						break
	
					row['no'] = stockno
					row['vol'] = row['vol'].replace(',','')
					row['turnover'] = row['turnover'].replace(',','') 	
					row['count'] = row['count'].replace(',','') 	
					db_conn.execute(ins_cmd, row)
					db_conn.commit()

db_conn.close()



