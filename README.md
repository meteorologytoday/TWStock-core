# TWStock
台灣股票抓取程式，作者XTT。

# 相依性
- Python3.4+
- Pip: sqlite3, Numpy, Matplotlib (optinal)
- Bash shell (可視需要自行修改)

# 初始設定操作順序
[環境設置] -> [掃描股市名稱] -> [抓取資料] -> [排列整理] -> [檔案後續分析]

# 環境設置
    > . setup.sh    # 純粹將src納入搜尋路徑

# 掃描股市名稱
    > ./scan.sh

# 抓取資料
    > ./script/download.sh                # 若無參數，預設抓取2個月的資料到STOCK.db
    > ./script/download.sh 12             # 抓取從今天往回推12個月資料，資料都會下載到STOCK.db

# 排列整理
    > # 將資料整理成一個一個Binary檔，依照股票編號輸出至data資料夾
    > # 另外也內插成「每日」資料(變成等時距)，存放至interp_data。科學分析可能較有需求
    > python3 src/reorder_data.py --database=STOCK.db

# 檔案後續分析

排列整理完畢後，每一檔股票將會依照自己的編號排成一個binary檔案，放在data資料夾。例如：台泥(1101)的檔案為data/1101.bin。Binary為32位元浮點數之排列。排列順序可在src/BinaryData.py裏頭的all_fields查詢到。目前排列為

1. 時間戳記 (unix timestamp)
2. 交易量
3. 交易額
4. 開盤價
5. 最高價
6. 最低價
7. 收盤價
8. 價差
9. 交易次數
10. 外資買進股數
11. 外資賣出股數
12. 投信買進股數
13. 投信賣出股數
14. 自營商買進股數(自行買賣)
15. 自營商賣出股數(自行買賣)
16. 自營商買進股數(避險)
17. 自營商賣出股數(避險)

# 資料夾結構
- data/        : 存放各股票的Binary資料檔
- interp_data/ : 存放各股票的Binary資料檔(內插成等時距)
- targets/     : 存放股票編號的清單
- src/         : 程式碼原始檔
- tools/       : 分析股票工具
- test/        : 測試程式碼
- web/         : (開發中) 網頁GUI，預計做成網頁介面控制
