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

	def addByTime(keys, arrs, time):
		"""
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
