import sys, getopt
from datetime import datetime
import BinaryData
import numpy as np
import matplotlib.pyplot as pplt

bin_file = None

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["bin="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--bin":
		bin_file = a

if bin_file is None:
	print("Must give paramter --bin")
	sys.exit(2)

# read data
data = BinaryData.readBinaryData(bin_file)

time_min, time_max = np.amin(data.time), np.amax(data.time)

time_scaled = (data.time - time_min) / 86400

x_label = [None for _ in data.time]

for i, time in enumerate(data.time):
	t = datetime.utcfromtimestamp(time)
	x_label[i] = t.strftime("%m/%d")

pplt.xlim([time_min - 86400, time_max + 86400])
pplt.xticks(data.time, x_label, rotation='vertical')
#candlestick2_ohlc(pplt.gca(), data.d['o_p'], data.d['c_p'], data.d['h_p'], data.d['l_p'])
pplt.plot(data.time, data.d['c_p'], marker='o', markersize=10)
pplt.plot(data.time, data.d['o_p'], marker='x', markersize=10)
pplt.show()
