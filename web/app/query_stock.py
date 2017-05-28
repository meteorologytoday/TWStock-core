import BinaryData
import re, os

def query(no, beg_date, end_date, dir_path):
	if re.match(r'^\d{4}$', no) is None:
		raise Exception("Invalid no")

	fname = "%s/%s.bin" % (dir_path, no)

	if not os.path.isfile(fname):
		raise Exception("Data does not exist.")

	return BinaryData.readBinaryData(fname)
