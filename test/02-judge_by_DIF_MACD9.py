import re
import sys, os
import getopt
from datetime import datetime
import numpy as np

from StockIO import StockReader
from StockLine import StockLine
from StockException import *

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a

if db_file is None:
	print("Must give paramter --database")
	sys.exit(2)


StRdr = StockReader(db_file)
StRdr.connectDB()

companies = StRdr.getListOfNo()
lines = []

for company in companies:
	data = None
	try:
		data = StRdr.readStockByNo(company)
	except NoStockDataException:
		print("Stock no %s has no data." % (company,))

	lines.append(StockLine(data, company))


over100 = []

for line in lines:
	vol = line.d['vol']
	if len(vol) < 3:
		continue

	avg = sum(vol[0:3]) / 3.0 / 1000.0

	if avg > 1000.0:
		print("%s : %d" % (line.no, int(avg),))
		over100.append(line)

print("Done loading %d stocks." % (len(lines),))
print("There are %d stocks over 100 vol in the past 3 days" % (len(over100),))
