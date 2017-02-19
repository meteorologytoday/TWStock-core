import re
import sys, os
import getopt
from datetime import datetime
import numpy as np

import read_data

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

all_data = read_data.read_data(in_dir)

for stockno, data in all_data.items():
	if len(data) != 9:
		print("%s is not good, only %d vars." % (stockno, len(data)))

