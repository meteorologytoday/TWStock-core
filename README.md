# TWStock
台灣股票抓取程式，作者XTT。

# 相依性
- Python3.4+
- Pip: sqlite3, Numpy, Matplotlib (optinal)
- Bash shell (可視需要自行修改)

# 初始設定操作順序
[抓取資料] -> [排列整理] -> [檔案後續分析]

# 環境設置
    > git clone https://github.com/meteorologytoday/TWStock-core.git
    > cd TWStock-core
    >
    > # 方法一：安裝至python
    > sudo python setup.py install
    >
    > # 方法二：純粹將src納入搜尋路徑
    > . setup.sh
    >
    > ./script/routine.sh 7  # 抓取資料

# 抓取資料
	> ./script/routine.sh [抓取天數(預設1天)] [資料庫之資料夾(預設為此專案之根目錄)]
    > ./script/routine.sh 2                  # 抓取兩天的股市資料至STOCK.db
    > ./script/routine.sh 20 /path/all_data  # 抓取20天之資料至 /path/all_data 資料夾

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
18. 前資餘額
19. 資買
20. 資賣
21. 現償
22. 融資限額
23. 前資餘額
24. 資買
25. 資賣
26. 現償
27. 融資限額
28. 當日交易(當沖)

# 資料夾結構
- targets/     : 存放股票編號的清單
- src/         : 程式碼原始檔
- test/        : 測試程式碼
