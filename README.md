# TWStock
台灣股票抓取程式，作者XTT

# 相依性
- Python3.4+, sqlite3 (pip package)
- Bash shell (可視需要自行修改)

# 初始設定操作順序
[環境設置] -> [掃描股市] -> [抓取資料] -> [排列整理] -> [檔案後續分析]

# 環境設置
    > . setup.sh    # 純粹將src納入搜尋路徑

# 掃描股市
    > ./scan.sh

# 抓取資料
    > ./script/download_foreground.sh  # 前景抓取
    > ./script/download.sh             # 背景抓取

# 排列整理
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
