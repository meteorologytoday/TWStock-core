import numpy as np

class Timeseries:
	"""
		Variable [time] is assumed to be ascending.
	"""
	def __init__(self, time, missing=-99999.0, dtype=np.float32):
		self.time = np.array(time, dtype=dtype)
		self.missing = dtype(missing)
		self.d = {}
		self.dtype = dtype

	def add(self, key, arr):
		if len(arr) != len(self.time):
			raise Error("Length of timeseries must be equal. (input: %d, it should be %d)" % (len(arr), len(self.time)))

		self.d[key] = np.array(arr, dtype=self.dtype)

	def addByTimeDict(self, keyarrs, time):
		keys, arrs = list(zip(*keyarrs.items()))
		self.addByTime(keys,arrs,time)


	def add(self, key, arr):
		if len(arr) != len(self.time):
			raise Exception("Added data must be the same size as time.")

		self.d[key] = np.array(arr, dtype=self.dtype)

	def addByTime(self, keys, arrs, time):
		"""
			This function add new data into timeseries. It first compare
			[time] with its own time points. The matched data will be stored,
			while the mismatched ones will be discarded. Missing data will
			be inserted as [Timeseries.missing]. If the key overlaps with
			original stored keys, new data overwrites.

			# keys

			# arrs
				All [arrs] must of same size

			# time
				[time] is assumed to be ascending for performance

		"""
		if len(keys) != len(arrs):
			print("ERROR! Length of keys must match length of arrs")
			return	
	

		# i-th element maps to mapping[i]-th element in arrs
		mapping = [None for _ in self.time]

		run_i = 0
		# Find insertion position
		for i in range(len(self.time)):
			try:
				while self.time[i] > time[run_i]:
					run_i += 1
			except IndexError:
				break
			
			if time[run_i] == self.time[i]:
				mapping[i] = run_i

		for i in range(0,len(keys)):
			key = keys[i]
			arr = arrs[i]
			new_arr = np.zeros(len(self.time), dtype=self.dtype)
			new_arr[:] =  self.missing
			for fr_i, to_i in enumerate(mapping):
				if not (to_i is None):
					new_arr[fr_i] = arr[to_i]

			self.d[key] = new_arr
		

	def pop(self, key):
		return self.d.pop(key)

	def __len__(self):
		return len(self.time)

	def printBinary(self, filename, keys=None):
		if keys is None:
			keys = list(self.d.keys())

		arr = np.zeros((len(self.time), len(keys)+1), dtype=np.float32)
		arr[:] = self.missing
		
		# notice we have to print data as a tuple list
		# (time[0], data1[0], data2[0], ...) (time[1], data1[1], data2[0], ...)
		# so the data should be arranged in special order
		arr[:, 0] = self.time
		for i, key in enumerate(keys):
			if key in self.d:
				arr[:,i+1] = self.d[key]
		
		arr.tofile(filename)

	

	def print(self, filename, keys=None):
		if keys is None:
			keys = list(self.d.keys())
		
		with open(filename, 'w') as f:
			f.write("# time ")
			for i in range(len(keys)):
				f.write("%s " % (keys[i],))
			f.write("\n")

			for i in range(len(self.time)):
				f.write("%f " % (self.time[i]))
				for key in keys:
					val = self.d[key][i]

					if val == self.missing:
						f.write("? ")
					else:
						f.write("%f " % (self.d[key][i]))
				f.write("\n")
