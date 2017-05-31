import os, sys, re
import TWStock.core.BinaryData as BinaryData

def data_iterator(dir_path='data'):
	parser = re.compile(r'(\d+)\.bin')
	for dirname, dirnames, filenames in os.walk(dir_path):
		for bin_file in filenames:
			m = parser.match(bin_file)
			if m is None:
				continue
	
			no = m.group(1)
	
			# read data
			data = BinaryData.readBinaryData('%s/%s' % (dir_path,bin_file,))
			
			yield (no, data)
