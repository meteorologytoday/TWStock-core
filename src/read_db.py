import sqlite3

class StockReader:
	def __init__(self, db_file, table):
		self.db_file = db_file
		self.table = table

	def getStock(self, no):
		sqlite3.connect(self.db_file)
		for row in sqlite3.execute("SELECT * FROM %s WHERE no = ? ORDER BY date DESC"):
			
		return 

