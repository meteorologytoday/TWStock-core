import re
import sys, os
import getopt
from datetime import datetime
import numpy as np

from StockIO import StockReader
from StockAnalyzer import StockAnalyzer
from TWSException import *

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a
try:
	db_file
except NameError:
	print("Must give paramter --database")
	sys.exit(2)


StRdr = StockReader(db_file)
StRdr.connectDB()

companies = StRdr.getListOfNo()
datum = []

for company in companies:
	data = None
	print(company)
	try:
		data = StRdr.readByNo(company)
	except NoDataException:
		print("Stock no %s has no data." % (company,))

	datum.append((company, data))


over100 = []

for data in datum:
	company, ts = data[0], data[1]
	vol = ts.d['vol']
	if len(vol) < 3:
		continue

	avg = sum(vol[0:3]) / 3.0 / 1000.0

	if avg > 1000.0:
		print("%s : %d" % (company, int(avg),))
		over100.append(data)

for data in over100:
	np.

print("Done loading %d stocks." % (len(datum),))
print("There are %d stocks over 1000 vol in the past 3 days" % (len(over100),))


