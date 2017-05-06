import sys, getopt
from StockShare import table_name as stock_table_name
from BizCorpShare import table_name as bizcorp_table_name
import BinaryData
import numpy as np
import sqlite3
from Timeseries import Timeseries


def copyStock(data, idx_from, idx_to):
	data['o_p'][idx_to] = data['o_p'][idx_from]
	data['c_p'][idx_to] = data['c_p'][idx_from]
	data['h_p'][idx_to] = data['h_p'][idx_from]
	data['l_p'][idx_to] = data['l_p'][idx_from]


def deducePrevStock(data, idx_pivot, prev_cnt):
	oc_p = data['o_p'][idx_pivot] - data['change_spread'][idx_pivot]
	data['o_p'][idx_pivot - prev_cnt:idx_pivot] = oc_p 
	data['c_p'][idx_pivot - prev_cnt:idx_pivot] = oc_p 
	data['h_p'][idx_pivot - prev_cnt:idx_pivot] = 0 
	data['l_p'][idx_pivot - prev_cnt:idx_pivot] = 0 



db_file = None

get_count_cmd = '''SELECT s.no, count(s.no) FROM ''' + stock_table_name + ''' AS s LEFT OUTER JOIN ''' + bizcorp_table_name + ''' AS b ON ( s.no = b.no AND s.date = b.date ) GROUP BY s.no ORDER BY s.no ASC;'''

# SELECT 順序必須完全符合 BinaryData.all_fields
get_data_cmd = '''SELECT s.date, s.vol, s.turnover, s.o_p, s.h_p, s.l_p, s.c_p, s.change_spread, s.count, b.foreign_i, b.foreign_o, b.trust_i, b.trust_o, b.dealer_self_i, b.dealer_self_o, b.dealer_hedge_i, b.dealer_hedge_o FROM ''' + stock_table_name + ''' AS s LEFT OUTER JOIN ''' + bizcorp_table_name + ''' AS b ON ( s.no = b.no AND s.date = b.date ) ORDER BY s.no ASC, s.date ASC;'''

fill_zeros = ['vol', 'turnover', 'change_spread', 'count', 'foreign_i', 'foreign_o', 'trust_i', 'trust_o', 'dealer_self_i', 'dealer_self_o', 'dealer_hedge_i', 'dealer_hedge_o']

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
print("正在從%s讀取資訊..." % (db_file,), end='')
c = sqlite3.connect(db_file)
data = list(zip(* c.execute(get_data_cmd).fetchall()))
no_count = c.execute(get_count_cmd).fetchall()
c.close()
print("完成。")

beg_i = 0
for i, (no, cnt) in enumerate(no_count):
	end_i = beg_i + cnt
	stock = Timeseries(data[0][beg_i:end_i])
	for j, field  in enumerate(BinaryData.all_fields):
		stock.add(field, data[j][beg_i:end_i])
	beg_i = end_i
	# 資料後處理
	# (1) 橋接當日無漲跌之股價
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

	# (2) 對於三大法人，NaN等同於0
	for key in fill_zeros:
		tmp = stock.d[key]
		for j, val in enumerate(tmp):
			if np.isnan(val):
				tmp[j] = 0.0

	# (3) 線性內插成每日資料
	#time_max, time_min = np.amax(stock.time), np.amin(stock.time)
	#new_time = np.arange(time_min, time_max + 1, 86400)
	#new_stock = Timeseries(new_time)
	#for key in stock.d:
#		new_stock.add(key, np.interp(new_time, stock.time, stock.d[key]))

	fname = "data/%s.bin" % (no,)
	print("正在寫入%s... " % (fname,), end='')
	stock.printBinary(fname, keys=BinaryData.data_fields)
	print("完成。")
	
