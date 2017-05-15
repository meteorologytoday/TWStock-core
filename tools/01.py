import os, sys, re, csv
import numpy as np

import BinaryData
from StockNames import name_table
import MathFuncs

candidates = []

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
			candidates.append([no, data.d['c_p'][-1]])

csvwriter = csv.writer(sys.stdout)
for candidate in candidates:
	csvwriter.writerow([candidate[0], name_table[candidate[0]], candidate[1]])
