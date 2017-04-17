import sqlite3
import StockShare
from TWSException import *
from Timeseries import Timeseries


ins_cmd = 'INSERT OR IGNORE INTO stocks(' + ','.join(StockShare.cols)+ ') VALUES (:' + ',:'.join(StockShare.cols) + ')'
sel_cmd = 'SELECT ' + ','.join(StockShare.sel_cols) + ' FROM stocks WHERE no = ? ORDER BY date desc'

class StockDownloader:

	def __init__(self, db_fname):
		self.db_fname = db_fname
		self.dbh = None
		self.valid_targets = []
		self.error_targets = []

	def __enter__(self):
		self.dbh = self.connectDB()
		return self

	def __exit__(self, extype, exvalue, extrace):
		self.dbh.close()	

	def connectDB(self):
		c = sqlite3.connect(self.db_fname)
		c.execute('''CREATE TABLE IF NOT EXISTS stocks (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			no TEXT,
			date INTEGER,
			vol REAL,
			turnover REAL,
			o_p REAL,
			h_p REAL,
			l_p REAL,
			c_p REAL,
			change_spread REAL,
			count REAL,
			UNIQUE(date, no)
		)''')
		c.commit()
		return c

	def writeDB(self, data):
		for row in data:
			self.dbh.execute(ins_cmd, row)
			self.dbh.commit()

	def resetTargets(self):
		self.valid_targets = []
		self.error_targets = []

	def addValidTarget(self, stockno, name):
		self.valid_targets.append([stockno, name])

	def addErrorTarget(self, stockno, desc):
		self.error_targets.append([stockno, desc])

	def printTargets(self, prefix, targets_dir='./'):
		valid_name = "%s/%s_valid_targets.csv" % (targets_dir, prefix, )
		error_name = "%s/%s_error_targets.csv" % (targets_dir, prefix, )
		with open(valid_name, 'w') as f:
			for target in self.valid_targets:
				f.write("%s,\"%s\"\n" % (target[0],target[1]))

		with open(error_name, 'w') as f:
			for stock in self.error_targets:
				f.write("%s, %s\n" % (stock[0], stock[1]))

		return valid_name, error_name
		

	def download(self, **kwargs):
		"""
		This method must be implemented to download data from various sites.

		# RETURN
		A list of stock data must be returned.

		"""
		raise NotImplementedError


class StockReader:
	
	def __init__(self, db_fname):
		self.db_fname = db_fname
		self.dbh = None
		self.valid_targets = []
		self.error_targets = []

	def __enter__(self):
		self.connectDB()
		return self

	def __exit__(self, extype, exvalue, extrace):
		self.disconnectDB()	

	def connectDB(self):
		self.dbh = sqlite3.connect(self.db_fname)

	def disconnectDB(self):
		self.dbh.close()

	def readByNo(self, no):
		tmp = list(zip(* self.dbh.execute(sel_cmd, (no, )).fetchall()))
		if len(tmp) != 0:
			result = Timeseries(tmp[0]) # 'date' column
			tmp
			for i, key in enumerate(StockShare.sel_cols[1:]):
				result.add(key, tmp[i+1])
			return result

		else:
			raise NoStockDataException("No data is available")

	def getListOfNo(self):
		return list(zip(*self.dbh.execute('''SELECT no FROM stocks GROUP BY no ORDER BY no ASC''').fetchall()))[0]

