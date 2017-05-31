table_name = 'BizCorp'
cols_desc = [
	('id',             'INTEGER PRIMARY KEY AUTOINCREMENT'),
	('no',             'TEXT'),       # 股票代號
	('date',           'INTEGER'),    # 時間
	('foreign_i',      'REAL'),       # 外資買進股數
	('foreign_o',      'REAL'),       # 外資賣出股數
	('trust_i',        'REAL'),       # 投信買進股數
	('trust_o',        'REAL'),       # 投信賣出股數
	('dealer_self_i',  'REAL'),       # 自營商買進股數(自行買賣)
	('dealer_self_o',  'REAL'),       # 自營商賣出股數(自行買賣)
	('dealer_hedge_i', 'REAL'),       # 自營商買進股數(避險)
	('dealer_hedge_o', 'REAL')        # 自營商賣出股數(避險)
]

create_cols     = [ ' '.join(cols_desc[i]) for i in range(0, len(cols_desc))]
ins_cols = [ cols_desc[i][0] for i in range(1, len(cols_desc))]
sel_cols = [ cols_desc[i][0] for i in range(2, len(cols_desc))]
uniq = ['no', 'date']
