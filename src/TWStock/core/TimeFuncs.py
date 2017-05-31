from datetime import *

def prevMonth(year, month, dmonth):
	"""
		Input and output are in the form of 
		base 1 = Jan, 2 = Feb, ..., 12 = Dec.
	"""
	dyear = int(dmonth / 12)
	m_residue = dmonth % 12

	if m_residue <= month - 1:
		return year-dyear, month - m_residue

	else:
		return year-dyear - 1, 12 + month  - m_residue


def iter_date(beg_date, end_date, include_end=True):
	beg_ts = int(beg_date.timestamp() / 86400) * 86400
	days = int(end_date.timestamp()/86400) - int(beg_date.timestamp()/86400) + ( 1 if include_end else 0 )
	for i in range(days):

		yield datetime.fromtimestamp(beg_ts)
		beg_ts += 86400
	

