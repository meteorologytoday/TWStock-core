import numpy as np

class StockWiz:
	def __init__(self, stock):
		self.stock = stock.copy()


	def ema(self, days, data=None):
		if data is None:
			data = self.stock

		smooth = 2.0 / (1.0 + days)
		ema = np.zeros(len(data))
		ema[0] = data[0]
		for i in range(1, len(data)):
			ema[i] = ema[i-1] + (data[i] - ema[i-1]) * smooth
		
		return ema

	def dif(self, s=12, l=26):
		return self.ema(s) - self.ema(l)

	def macd(self, days=9):	
		return self.ema(days, self.dif())

	
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
