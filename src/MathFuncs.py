import numpy as np

class mixAnalysis:
	def genAnalysis(self):
		self.d['dif']  = dif(self.d['c_p'])
		self.d['macd'] = ema(self.d['dif'], 9)
		self.d['mva005'] = mva(self.d['c_p'],  5)
		self.d['mva010'] = mva(self.d['c_p'], 10)
		self.d['mva020'] = mva(self.d['c_p'], 20)
		self.d['mva060'] = mva(self.d['c_p'], 60)

def mva(data, days):
	result = np.zeros(len(data))
	result[0:days-1] = np.nan
	for i in range(days-1, len(result)):
		result[i] = data[i+1-days:i+1].sum() / days
	return result

def ema(data, days):
	smooth = 2.0 / (1.0 + days)
	result = np.zeros(len(data))
	result[0] = data[0]
	for i in range(1, len(data)):
		result[i] = result[i-1] + (data[i] - result[i-1]) * smooth
	
	return result

def dif(data, s=12, l=26):
	return ema(data, s) - ema(data, l)

def findCrx(data1, data2, detect_days=1):
	"""
	This function finds the crossing point (+1 for upward, -1 for downward)
	in [detect_days] days. Note that upward crossing means data1 penetrates
	data2 at sometime between detection region and vice versa.
	"""
	if detect_days <= 0:
		error('detect_days must be positive integer.')

	tmp = data1 - data2
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
