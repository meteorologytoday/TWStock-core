def readFile(fname):
	time = []
	data = []
	
	with open(fname, 'r') as f:
		for l in f:
			tmp = l.split()
			time.append(tmp[1])
			data.append(float(tmp[2]))
	return time, data
