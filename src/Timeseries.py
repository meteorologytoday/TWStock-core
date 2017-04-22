import numpy as np

class Timeseries:
	"""
		Variable [time] is assumed to be ascending.
	"""
	def __init__(self, time, missing=-999):
		self.time = np.array(time)
		self.missing = missing
		self.d = {}

	def add(self, key, arr):
		if len(arr) != len(self.time):
			raise Error("Length of timeseries must be equal. (input: %d, it should be %d)" % (len(arr), len(self.time)))

		self.d[key] = np.array(arr, dtype=float)

	def addByTimeDict(self, keyarrs, time):
		keys, arrs = list(zip(*keyarrs.items()))
		self.addByTime(keys,arrs,time)

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

		mapping = [None for _ in time]

		run_i = 0
		len_time = len(time)

		# Find insertion position
		for i in range(0, len_time):
			try:
				while time[i] > self.time[run_i]:
					run_i += 1
			except IndexError:
				break
			
			if time[i] == self.time[run_i]:
				mapping[i] = run_i

		for i in range(0,len(keys)):
			key = keys[i]
			arr = arrs[i]
			new_arr = np.zeros(len(self.time), dtype=float) + self.missing
			for fr_i, to_i in enumerate(mapping):
				if not (to_i is None):
					new_arr[fr_i] = arr[to_i]

			self.d[key] = new_arr
		

	def pop(self, key):
		return self.d.pop(key)

	def __len__(self):
		return len(self.time)

	def print(self, filename):
		keys = list(self.d.keys())
		with open(filename, 'w') as f:
			f.write("# time ")
			for i in range(len(keys)):
				f.write("%s " % (keys[i],))
			f.write("\n")

			for i in range(len(self.time)):
				f.write("%f " % (self.time[i]))
				for key in keys:
					f.write("%f " % (self.d[key][i]))
				f.write("\n")
