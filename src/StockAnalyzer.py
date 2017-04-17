import numpy as np
import StockShare
import Timeseries
from MathFuncs import *


class StockAnalyzer:
	def __init__(self, ts):
		self.ts = ts
	
	def macd(data, days=9):
		return ema(self.ts.d['c_p'], days)

"""
	def fastSlowCrx(self, detect_days=1):
		if detect_days <= 0:
			error('detect_days must be positive integer.')
	
		tmp = self.dif() - self.macd()
		n = len(tmp) - 1
		# element 0 correspond to the latest day, 1 the previous one day, and so on
		signal = np.zeros(detect_days)
		
		for day_shift in range(0, detect_days):
			current = n - day_shift
			if tmp[current -1] < 0 and tmp[current] >= 0:
				signal[day_shift] = 1
			elif tmp[current -1] >= 0 and tmp[current] < 0:
				signal[day_shift] = -1

		return signal if detect_days > 1 else signal[0]
"""
