import re
import sys, os
import getopt
from datetime import datetime
import read_single_data as rsd
import numpy as np
try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["input-dir="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

in_dir = None

for o, a in opts:
	if o == "--input-dir":
		in_dir = a

if in_dir is None:
	print("Must give paramter --input-dir")
	sys.exit(2)

pattern = re.compile(r'(?P<stockno>\d+)-(?P<var>[a-zA-Z0-9_]+)\.txt')

all_data = {}
c=0
for subdir, dirs, files in os.walk(in_dir):
	for f in files:
		full_fname = "%s/%s" % (in_dir, f)
		m = pattern.match(f)
		if m:
			time, data = rsd.readFile(full_fname)
			print("File [%s] is successfully read." % (full_fname,))
			stockno = m.group('stockno')
			var = m.group('var')
			if not stockno in all_data:
				all_data[stockno] = {}
	
			all_data[stockno][var] = [time, np.array(data)]
			c += 1
		else:
			print("File [%s] might not be a valid file." % (full_fname,))

	
print("%d files were successfully read." % (c,))
print("There are %d stock number were read." % (len(all_data),))

for stockno, data in all_data.items():
	if len(data) != 9:
		print("%s is not good, only %d vars." % (stockno, len(data)))

#print(sorted(all_data.keys()))
