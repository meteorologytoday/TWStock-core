import os, sys, re
from datetime import datetime
import BinaryData
import numpy as np
from StockNames import name_table
import MathFuncs

nos = []

parser = re.compile(r'(\d+)\.bin')
for dirname, dirnames, filenames in os.walk('data'):
	for bin_file in filenames:
		m = parser.match(bin_file)
		if not m:
			continue

		no = m.group(1)

		# read data
		data = BinaryData.readBinaryData('data/%s' % (bin_file,))
		data.genAnalysis()

		sig_crx3 = (MathFuncs.findCrx(data.d['dif'], data.d['macd'], 3) == 1).any()
		sig_foreign_buy3 = ((data.d['foreign_i'][-3:] - data.d['foreign_o'][-3:]) > 10000).all()


		if sig_crx3 and sig_foreign_buy3:
			#print(no)
			#print(data.d['foreign_i'][-3:])
			nos.append(no)

for no in nos:
	print("%s (%s)" % (no, name_table[no]))

print("Total %d result(s)." % (len(nos),))
