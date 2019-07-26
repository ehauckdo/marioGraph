class Node:

	def __init__(self):
		pass

	def __init__(self, x, y, tile=None, type="P"):
		self.x = x
		self.y = y
		self.tile = tile
		self.type = type

	#def __init__(self, x, y, t):
	#	self.x = x
	#	self.y = y
	#	self.type = t # sprite_id

	def __repr__(self):
		return "{},{}".format(self.x, self.y)

