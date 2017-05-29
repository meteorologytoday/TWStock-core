import sys, csv
import numpy as np

import BinaryData
from StockNames import name_table
import MathFuncs
from iterators import data_iterator

candidates = []

for (no, data) in data_iterator('data'):

	if len(data.time) < 7:
		print("Skip. %s has few data: %d" % (no, len(data.time)))
		continue

	data.genAnalysis()
	
	if sig_crx3 and sig_foreign_buy3:
		candidates.append([no, data.d['c_p'][-1]])

csvwriter = csv.writer(sys.stdout)
for candidate in candidates:
	csvwriter.writerow([candidate[0], name_table[candidate[0]], candidate[1]])
