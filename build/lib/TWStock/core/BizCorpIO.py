import sqlite3
import BizCorpShare
from Timeseries import Timeseries
from TWSException import *

ins_cmd = 'INSERT OR IGNORE INTO ' + BizCorpShare.table_name + '(' + ','.join(BizCorpShare.ins_cols)+ ') VALUES (:' + ',:'.join(BizCorpShare.ins_cols) + ')'
sel_cmd = 'SELECT ' + ','.join(BizCorpShare.sel_cols) + ' FROM ' + BizCorpShare.table_name + ' WHERE no = ? ORDER BY date ASC'
create_cmd = 'CREATE TABLE IF NOT EXISTS ' + BizCorpShare.table_name \
	+ ' (' + (','.join(BizCorpShare.create_cols)) \
	+ ', UNIQUE(' + (','.join(BizCorpShare.uniq)) + ') )'

class BizCorpDownloader:

	def __init__(self, db_fname):
		self.db_fname = db_fname
		self.dbh = None

	def __enter__(self):
		self.dbh = self.connectDB()
		return self

	def __exit__(self, extype, exvalue, extrace):
		self.dbh.close()	

	def connectDB(self):
		c = sqlite3.connect(self.db_fname)
		c.execute(create_cmd)
		c.commit()
		return c

	def writeDB(self, data):
		print("寫入%d筆資料" % (len(data),))
		for row in data:
			self.dbh.execute(ins_cmd, row)
			self.dbh.commit()

	def download(self, **kwargs):
		"""
		This method must be implemented to download data from various sites.

		# RETURN
		A list of stock data must be returned.

		"""
		raise NotImplementedError


class BizCorpReader:
	
	def __init__(self, db_fname):
		self.db_fname = db_fname
		self.dbh = None

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
		result = {}

		tmp = list(zip(* self.dbh.execute(sel_cmd, (no, )).fetchall()))
		if len(tmp) != 0:
			result = Timeseries(tmp.pop(0)) # 'date' column
			for i, key in enumerate(BizCorpShare.sel_cols[1:]):
				result.add(key, tmp[i])
			return result

		else:
			raise NoDataException("No data is available")

	def getListOfNo(self):
		return list(zip(*self.dbh.execute('SELECT no FROM ' + BizCorpShare.table_name + ' GROUP BY no ORDER BY no ASC').fetchall()))[0]

