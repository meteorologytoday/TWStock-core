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
			ema[i] = ema[i-1] * (1 - smooth) + data[i] * smooth
		
		return ema

	def dif(self, s=12, l=26):
		return self.ema(s) - self.ema(l)

	def macd(self, days=9):	
		return self.ema(days, self.dif())
