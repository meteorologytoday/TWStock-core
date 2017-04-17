import numpy as np

def ema(data, days):
	smooth = 2.0 / (1.0 + days)
	result = np.zeros(len(data))
	result[0] = data[0]
	for i in range(1, len(data)):
		result[i] = result[i-1] + (data[i] - result[i-1]) * smooth
	
	return result

def dif(data, s=12, l=26):
	return ema(data, s) - ema(data, l)
