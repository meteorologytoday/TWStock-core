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
	sig_crx3 = (MathFuncs.findCrx(data.d['dif'], data.d['macd'], 3) == 1).any()
	sig_foreign_buy3 = ((data.d['foreign_i'][-3:] - data.d['foreign_o'][-3:]) > 10000).all()

	vol_avg = np.sum(data.d['vol'][-5:]) / 5.0
	foreign_net = data.d['foreign_i'][-1] - data.d['foreign_o'][-1]
	sig_vol = True if vol_avg > 0 and foreign_net / vol_avg > 0.1 else False
			
	if sig_crx3 and sig_foreign_buy3 and sig_vol:
		candidates.append([no, data.d['c_p'][-1], vol_avg, foreign_net])

csvwriter = csv.writer(sys.stdout)

for candidate in candidates:
	csvwriter.writerow([candidate[0], name_table[candidate[0]], candidate[1], candidate[2] / 1000.0, candidate[3]/1000.0])
