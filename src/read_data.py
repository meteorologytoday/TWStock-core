import re, sys, os, csv
import sys, os
import getopt
from datetime import datetime
import numpy as np

def read_data(in_dir):

	if in_dir is None:
		print("Must give paramter in_dir")
		sys.exit(2)
	
	pattern = re.compile(r'(?P<stockno>\d+)\.csv')
	all_data = {}
	c=0
	for subdir, dirs, files in os.walk(in_dir):
		for f in files:
			full_fname = "%s/%s" % (in_dir, f)
			m = pattern.match(f)
			if m:
				time = []
				data = []

				with open(full_fname, 'r') as csvfile:
					csvreader = csv.DictReader(csvfile)
					for line in csvreader:
						time.append(int(line['timestamp']))
						data.append(float(line['Close_D']))

				#print("File [%s] is successfully read." % (full_fname,))
				stockno = m.group('stockno')
				if not stockno in all_data:
					all_data[stockno] = {}
		
				all_data[stockno] = [time, np.array(data)]
				c += 1
			else:
				print("File [%s] might not be a valid file." % (full_fname,))
	
		
	print("%d files were successfully read." % (c,))
	print("There are %d stock number were read." % (len(all_data),))
	
	return all_data

