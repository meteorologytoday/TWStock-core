import urllib.parse
import urllib.request
import json
import re
import sys, os
from datetime import datetime

os.makedirs('data') if not os.path.exists('data') else None
output_dir = "data/%s" % (datetime.now().strftime("%Y%m%d"),)
os.makedirs(output_dir) if not os.path.exists(output_dir) else None

url = 'http://%s%s' % ('www.wantgoo.com', urllib.parse.quote('/Stock/個股線圖/技術線圖資料') )

targets = []

for target in sys.stdin:
	stockno, name = target.split(',')
	name = name.strip()
	stockno = int(stockno)
	targets.append([name, stockno])

params = {
	'Kcounts'      : 120,
	'Type'         : '日K_K線|日K_漲跌資料|日K_成交量|日K_KD|日K_RSI|日K_MACD',
	'isCleanCache' : 'false',
	'StockNo'      : None
}

series = ['K9_D', 'D9_D', 'Mean5_D', 'Mean10_D', 'Mean20_D', 'Mean60_D', 'Mean120_D', 'MACD_DIF_D', 'MACD_MACD9_D']

for (name, stockno) in targets:
	print("收集[%s]的股市資料(編號%d)" % (name, stockno))
	
	params['StockNo'] = "%04d" % (stockno,)

	data = urllib.parse.urlencode(params)
	data = data.encode('ascii') # data should be bytes


	
	req = urllib.request.Request(url, data)
	
	jsonstr = []
	
	with urllib.request.urlopen(req) as response:
		x = response.read()
		jsonstr.append(x)
		
	
	decoder = json.JSONDecoder
	
	jsonstr = b''.join(jsonstr).decode('utf-8')
	
	raw_data = json.loads(jsonstr)['returnValues']['value']
	
	# parse
	data = {}
	raw_data = re.sub(r'(?:<script>|</script>)', '', raw_data, flags=re.ASCII);

	for m in re.finditer(r'var\s+(?P<var>[\w_]+)\s*=\s*(?P<list>[^;]+?)\s*;', raw_data):
		gd = m.groupdict()
		
	#	print("var: %s, data: %s", (gd['var'], gd['list']))
	
		if gd['var'] in series:
			print("Got series \"%s\"" % gd['var'])
			if gd['list'] == '[]':
				print("Empty data, jump to next data...")
				continue

			meta_time = []
			meta_data = []
			
			for row in gd['list'][2:-2].split('],['):
				row_split = row.split(',')
				#print(row_split)
				meta_time.append(row_split[0])
				meta_data.append(row_split[1])
			
			data[gd['var']] = [meta_time, meta_data]
	
	for key, val in data.items():
		with open("%s/%d-%s.txt" % (output_dir, stockno, key), 'w') as f:
			for i in range(0, len(val[0])):
				f.write("%d %s %s\n" % (i, datetime.fromtimestamp(int(val[0][i])/1000).strftime("%Y-%m-%d"), val[1][i]))
