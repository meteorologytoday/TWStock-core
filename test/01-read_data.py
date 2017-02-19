import re
import sys, os
import getopt
from datetime import datetime
import numpy as np

import read_data
from tools import StockWiz

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["input-dir="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

in_dir = None

for o, a in opts:
	if o == "--input-dir":
		in_dir = a

if in_dir is None:
	print("Must give paramter --input-dir")
	sys.exit(2)

all_data = read_data.read_data(in_dir)

for stockno, data in all_data.items():
	if len(data[0]) == 0:
		print("Stock %s is empty, continue to next." % (stockno,))
		continue

	if int(stockno) != 2301:
		continue

	w = StockWiz(data[1])
	print("stocknumber: %s" % (stockno, ))
	print(data[1])
	print("EMA")
	print(w.ema(10))
	print(w.dif())
	print(w.macd())

#print(sorted(all_data.keys()))
