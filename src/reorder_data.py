import sys, getopt
from StockIO import StockReader
from BizCorpIO import BizCorpReader
from TWSException import *
import BinaryData
import numpy as np

db_file = None

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["database="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

for o, a in opts:
	if o == "--database":
		db_file = a

if db_file is None:
	print("Must give paramter --database")
	sys.exit(2)


stocks = {}
bizcorps = {}

print("正在讀取個股資訊")
# Read Stock
with StockReader(db_file) as reader:
	stock_symbols = reader.getListOfNo()
	
	for stock_symbol in stock_symbols:
		stocks[stock_symbol] = reader.readByNo(stock_symbol)

print("正在讀取三大法人資訊")
# Read BizCorp
with BizCorpReader(db_file) as reader:
	stock_symbols = reader.getListOfNo()

	for stock_symbol in stock_symbols:
		bizcorps[stock_symbol] = reader.readByNo(stock_symbol)




bizcorp_keys = bizcorps.keys()

copy_items = ['o_p', 'c_p', 'h_p', 'l_p']
def copyStock(data, idx_from, idx_to):
	global copy_items
	for item in copy_items:
		data[item][idx_to] = data[item][idx_from]

def deducePrevStock(data, idx_pivot, prev_cnt):
	oc_p = data['o_p'][idx_pivot] - data['change_spread'][idx_pivot]
	data['o_p'][idx_pivot - prev_cnt:idx_pivot] = oc_p 
	data['c_p'][idx_pivot - prev_cnt:idx_pivot] = oc_p 
	data['h_p'][idx_pivot - prev_cnt:idx_pivot] = 0 
	data['l_p'][idx_pivot - prev_cnt:idx_pivot] = 0 

fill_zeros = ['foreign_i', 'foreign_o', 'trust_i', 'trust_o', 'dealer_self_i', 'dealer_self_o', 'dealer_hedge_i', 'dealer_hedge_o']
for stock_symbol, stock  in stocks.items():
#	print("正在處理 %s " % (stock_symbol,))

	if stock_symbol in bizcorp_keys:
		bizcorp = bizcorps[stock_symbol]
		stock.addByTimeDict(bizcorp.d, bizcorp.time)

	# 橋接當日無漲跌之股價
	tmp = stock.d['c_p']
	prev_nan = np.isnan(tmp[0])
	prev_nan_cnt = 1 if prev_nan else 0
	if not np.isnan(tmp).all(): # 至少要有一筆資料才能推算
		for i in range(1, len(tmp)):

			now_nan = np.isnan(tmp[i])
			if (not prev_nan) and now_nan:    # 複製前日資料
				copyStock(stock.d, i-1, i)
			elif prev_nan and now_nan:        # 連續發現NaN    注意只有從頭就是NaN才會落入此一狀況
				prev_nan_cnt += 1
			elif prev_nan and (not now_nan):   # 回推前數日資料 注意只有從頭就是NaN才會落入此一狀況
				deducePrevStock(stock.d, i, prev_nan_cnt)

			# 記得將前一次的判斷暫存起來
			prev_nan = now_nan


	if stock_symbol == '6103':
		print(stock.d['foreign_i'])

	# 對於三大法人資訊，missing即為0
	for key in fill_zeros:
		if not (key in stock.d): # 若無則跳過
			continue

		tmp = stock.d[key]
		for i, val in enumerate(tmp):
			if val == stock.missing:
				tmp[i] = 0.0


	if stock_symbol == '6103':
		print(stock.d['foreign_i'])
	fname = "data/%s.bin" % (stock_symbol,)
	#print("Writing to %s... " % (fname,), end='')
	stock.printBinary(fname, keys=BinaryData.data_fields)
	#print("done")
