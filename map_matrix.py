import logging
import logger
import inspect	

class MapMatrix:

	def __init__(self):
		pass

	def __init__(self, filename):
		self.map = self.read_map(filename)

	def initialize_map(self, x_length, y_length):
		logger.init(self, inspect.stack()[0][3])

		map = []
		for y in range(y_length):
			row = []
			for x in range(x_length):
				row.append("-")
			map.append(row)
		map[-2][2] = "M"

		logger.end(self, inspect.stack()[0][3])
		return map

	def read_map(self, filename):
		logger.init(self, inspect.stack()[0][3])

		logging.info("Parsing {}".format(filename))
		map = []
		input_file = open(filename)
		for line in input_file:
			map.append([])
			# line[-1] avoids getting the /n at the end
			for char in line[:-1]:
				map[-1].append(char)

		self.y_length = len(map)
		self.x_length = len(map[0])
	
		logger.end(self, inspect.stack()[0][3])
		return map

	def print_map(self):
		logger.init(self, inspect.stack()[0][3])
		print("Printing current map...")
		print("X tile length: {}, Y tile length: {}".format(self.x_length, self.y_length))
		for line in self.map:
			x_string = ""
			for char in line:
				x_string += char
			print(x_string)
		
		logger.end(self, inspect.stack()[0][3])