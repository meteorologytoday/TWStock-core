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

