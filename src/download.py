import sys
from TWSEDownloader import TWSEDownloader
from TPEXDownloader import TPEXDownloader

with TPEXDownloader('STOCK.db') as handler:
	handler.download(months=1, targets=sys.argv[1])
	handler.printTargets('TPEX')

with TWSEDownloader('STOCK.db') as handler:
	handler.download(months=12, targets=sys.argv[1])
	handler.printTargets('TWSE')

print("下載完成！")
