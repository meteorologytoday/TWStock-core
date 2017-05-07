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
print(len(data.time))

data.genAnalysis()

days = 80
times = data.time[-days:]
order = np.arange(0, len(times))
c_p = data.d['c_p'][-days:]
dif = data.d['dif'][-days:]
macd = data.d['macd'][-days:]
mva5  = data.d['mva005'][-days:]
mva10 = data.d['mva010'][-days:]
mva20 = data.d['mva020'][-days:]
mva60 = data.d['mva060'][-days:]

time_label = [None for _ in times]

for i, time in enumerate(times):
	t = datetime.utcfromtimestamp(time)
	time_label[i] = t.strftime("%m/%d")

fig, (ax1, ax2) = pplt.subplots(2, sharex=True)
#fig.subplots_adjust(hspace=0)

ax1.set_title(bin_file)
ax1.set_ylim([np.amin(c_p)-2, np.amax(c_p) + 2])
ax2.set_xlim([order[0]-1, order[-1]+1])
ax2.set_xticks(order)
ax2.set_xticklabels(time_label, rotation=90)

ax1.plot(order, c_p  , marker='o', markersize=2, color='k')
ax1.plot(order, mva5 , marker='o', markersize=2, color='r')
ax1.plot(order, mva10, marker='o', markersize=2, color='g')
ax1.plot(order, mva20, marker='o', markersize=2, color='b')
ax1.plot(order, mva60, marker='o', markersize=2, color='k', dashes=(10,3))
ax2.plot(order, dif , marker='o', markersize=2, markerfacecolor='b', color='b')
ax2.plot(order, macd, marker='x', markersize=2, markerfacecolor='r', color='r')

pplt.show()
