import urllib.parse
import urllib.request
import json, re, sys, csv

def defaultIterator():
	for i in range(1, 10):
		yield '%d' % (i,)

no_filter = re.compile(r'^\d{4}$')
def scanNames(iterator=None):
	global no_filter
	mapping = {}

	if iterator is None:
		iterator = defaultIterator

	for no in iterator():
		print("掃描TWSE%s" % (no,))
		params = urllib.parse.urlencode({
			'query'  : no
		})

		req = urllib.request.Request(
			'http://www.twse.com.tw/zh/api/codeQuery?' + params
		)

		try:
			with urllib.request.urlopen(req, timeout=10) as response:
				data = json.loads(response.read().decode())
		except urllib.error.URLError as e:
			raise Exception("URL 錯誤")
		except timeout as e:
			raise Exception("長時間無回應")

		for sug in data['suggestions']:
			sp = sug.split('\t')
			if no_filter.match(sp[0]) is not None and len(sp) == 2:
				mapping[sp[0]] = sp[1]

	for no in defaultIterator():
		print("掃描TPEX%s" % (no,))
		params = urllib.parse.urlencode({
			'term'  : no,
			'l'     : 'zh-tw',
		})

		req = urllib.request.Request(
			'http://www.tpex.org.tw/web/inc/search_stk_reg_all.php?' + params
		)

		try:
			with urllib.request.urlopen(req, timeout=10) as response:
				data = json.loads(response.read().decode())
		except urllib.error.URLError as e:
			raise Exception("URL 錯誤")
		except timeout as e:
			raise Exception("長時間無回應")

		for sug in data:
			if no_filter.match(sug['value']) is not None:
				mapping[sug['value']] = sug['label'].split(' ')[1]

	return mapping

def loadNames(filename):
	name_table = {}
	with open(filename, 'r') as f:
		for row in csv.DictReader(f, ['no', 'name']):
			name_table[row['no']] = row['name']
	return name_table

if __name__ == '__main__':
	fname = 'mapping.csv' if len(sys.argv) < 2 else sys.argv[1]
	print("結果將存至%s" % (fname,)) 

	mapping = scanNames()
	keys = sorted(mapping.keys())

	with open(fname, 'w') as f:
		writer = csv.writer(f)
		for key in keys:
			writer.writerow([key, mapping[key]])

		
	print("作業完成") 
