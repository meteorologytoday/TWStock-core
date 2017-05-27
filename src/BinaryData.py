import numpy as np
from Timeseries import Timeseries as TS

dtype = np.float32
missing = np.nan

all_fields = [
	'date',
	'vol',
	'turnover',
	'o_p',
	'h_p',
	'l_p',
	'c_p',
	'change_spread',
	'count',
	'foreign_i',
	'foreign_o',
	'trust_i',  
	'trust_o',  
	'dealer_self_i',
	'dealer_self_o',
	'dealer_hedge_i',
	'dealer_hedge_o',
	'fin_pb',
	'fin_b',
	'fin_s',
	'fin_r',
	'fin_l',
	'mar_pb',
	'mar_b',
	'mar_w',
	'mar_r',
	'mar_l',
	'day_trade',
]

data_fields = all_fields[1:]

def readBinaryData(filename):
	global dtype, all_fields, missing
	data = np.fromfile(filename, dtype=dtype)
	if len(data) % len(all_fields) != 0:
		raise Exception("Error: there should be multiple of %d data. %d data were read." % (len(all_fields), len(data)))

	n = len(data) / len(all_fields)
	data = data.reshape((n, len(all_fields))).transpose()
	
	ts = TS(data[0,:], missing=missing, dtype=dtype)

	for i, key in enumerate(data_fields):
		ts.add(key, data[i+1,:]) # skip timestamp field

	return ts
