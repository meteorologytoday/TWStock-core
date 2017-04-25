import sys, getopt
from StockIO import StockReader
from BizCorpIO import BizCorpReader
from TWSException import *


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
# Read Stock
with StockReader(db_file) as reader:
	stock_symbols = reader.getListOfNo()
	
	for stock_symbol in stock_symbols:
		stocks[stock_symbol] = reader.readByNo(stock_symbol)

# Read BizCorp
with BizCorpReader(db_file) as reader:
	stock_symbols = reader.getListOfNo()

	for stock_symbol in stock_symbols:
		bizcorps[stock_symbol] = reader.readByNo(stock_symbol)




bizcorp_keys = bizcorps.keys()
for stock_symbol, stock  in stocks.items():
	if stock_symbol in bizcorp_keys:
		bizcorp = bizcorps[stock_symbol]
		stock.addByTimeDict(bizcorp.d, bizcorp.time)

print(stocks['1101'].d['foreign_o'])
stocks['1101'].print('1101.txt', ['dealer_self_i', 'foreign_i'])
	
