import csv

def loadNameTable(name):
	name_table = {}
	for filename in ['TPEX_SCAN_valid_targets.csv', 'TWSE_SCAN_valid_targets.csv']:
		with open('targets/%s' % (filename,), 'r') as f:
			for row in csv.DictReader(f, ['no', 'name']):
				name_table[row['no']] = row['name']

	return name_table
