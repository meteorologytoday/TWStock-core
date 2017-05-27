table_name = 'FinMar'
cols_desc = [
	('id',             'INTEGER PRIMARY KEY AUTOINCREMENT'),
	('no',             'TEXT'),       # 股票代號
	('date',           'INTEGER'),    # 時間
	('fin_pbal',       'REAL'),       # 前資餘額(股) (previous balance)
	('fin_b',          'REAL'),       # 資買 (buy)
	('fin_s',          'REAL'),       # 資賣 (sell)
	('fin_r',          'REAL'),       # 現償 (repay)
	('fin_l',          'REAL'),       # 資限額 (limit)
	('mar_pbal'        'REAL'),       # 前券餘額(股) (previous balance)
	('mar_b',          'REAL'),       # 券買 (buy)
	('mar_s',          'REAL'),       # 券賣 (sell)
	('mar_r',          'REAL'),       # 券償 (repay)
	('mar_l',          'REAL'),       # 券限額 (limit)
	('day_trade',      'REAL'),       # 當日交易 (當沖)
]

create_cols     = [ ' '.join(cols_desc[i]) for i in range(0, len(cols_desc))]
ins_cols = [ cols_desc[i][0] for i in range(1, len(cols_desc))]
sel_cols = [ cols_desc[i][0] for i in range(2, len(cols_desc))]
uniq = ['no', 'date']
