import urllib.parse
import urllib.request
import json, re, sys, os, csv
from datetime import datetime

os.makedirs('data') if not os.path.exists('data') else None
output_dir = "data/%s" % (datetime.now().strftime("%Y%m%d"),)
os.makedirs(output_dir) if not os.path.exists(output_dir) else None

url = 'http://%s%s' % ('www.wantgoo.com', urllib.parse.quote('/Stock/個股線圖/技術線圖資料') )

print("Going to read %s" % (sys.argv[1],))



params = {
	'Kcounts'      : 120,
	'Type'         : '日K_K線|日K_漲跌資料|日K_成交量|日K_KD|日K_RSI|日K_MACD',
	'isCleanCache' : 'false',
	'StockNo'      : None
}

#series = ['K9_D', 'D9_D', 'Mean5_D', 'Mean10_D', 'Mean20_D', 'Mean60_D', 'Mean120_D', 'MACD_DIF_D', 'MACD_MACD9_D']

valid_targets = ['Close_D']
with open(sys.argv[1], 'r') as target_file:
	for stock in csv.DictReader(target_file, ['stockno', 'name']):
		name = stock['name']
		stockno = int(stock['stockno'])
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
		data = []
		raw_data = re.sub(r'(?:<script>|</script>)', '', raw_data, flags=re.ASCII);
	
		for m in re.finditer(r'var\s+(?P<var>[\w_]+)\s*=\s*(?P<list>[^;]+?)\s*;', raw_data):
			gd = m.groupdict()
			
		#	print("var: %s, data: %s", (gd['var'], gd['list']))
		
			if gd['var'] == 'Close_D':
				print("Got series Close_D")
				if gd['list'] == '[]':
					print("Empty data, jump to next data...")
					continue
				
				for row in gd['list'][2:-2].split('],['):
					data.append(row.split(','))
				
		if len(data) == 0:
			print("No data for stockno %d" % (stockno,))
		else:
			valid_targets.append([stockno, 'Unknown'])
			with open("%s/%d.csv" % (output_dir, stockno), 'w') as f:
				csvwriter = csv.writer(f)
				csvwriter.writerow(['timestamp', 'timestring', 'Close_D'])
				for i, val in enumerate(data):
					csvwriter.writerow([val[0], datetime.fromtimestamp(int(val[0])/1000).strftime("%Y-%m-%d"), val[1]])
	
with open("valid_targets.csv", 'w') as f:
	csvwriter = csv.writer(f)
	for i, val in enumerate(valid_targets):
		csvwriter.writerow([val[0], val[1]])
