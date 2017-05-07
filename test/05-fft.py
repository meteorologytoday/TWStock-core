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

c_p = data.d['c_p'].copy()
m = (c_p[-1] - c_p[0]) / (len(c_p) - 1)
c_p -= m * np.arange(0, len(c_p))


# doing fft
spectrum = abs(np.fft.rfft(c_p)[1:])
print(len(spectrum))
wavenumber = np.log(np.arange(0, len(spectrum))+1)


wn_labeled      = np.log(len(c_p) / np.array([7, 30, 30.5*3, 30.5*6, 365]))
wn_labeled_text = ['weekly', 'monthly', 'seasonly', 'half year', 'yearly'] 

time_min, time_max = np.amin(data.time), np.amax(data.time)
time_scaled = (data.time - time_min) / 86400

time_label = [None for _ in data.time]

for i, time in enumerate(data.time):
	t = datetime.utcfromtimestamp(time)
	time_label[i] = t.strftime("%m/%d")

fig, (ax1, ax2) = pplt.subplots(2)
#fig.subplots_adjust(hspace=0)

ax1.set_title(bin_file)
ax1.set_xlim([time_min - 86400, time_max + 86400])
ax1.set_xticks(data.time)
ax1.set_xticklabels(time_label, rotation=45)

ax2.set_xticks(wn_labeled)
ax2.set_xticklabels(wn_labeled_text, rotation=0)

ax1.plot(data.time, c_p, marker='o', markersize=2, color='b')
ax1.plot(data.time, data.d['c_p'], marker='o', markersize=2, color='r')

ax2.plot(wavenumber, spectrum)
pplt.show()
