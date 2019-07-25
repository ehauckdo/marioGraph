from node import Node
import helper.logger as logger
import logging
import inspect	

# receives a list of positions (x,y) of interactable blocks
# return nodes and edges (as tuples) representing them
def interactable_to_graph(block_list):
	logger.init_m(__file__,inspect.stack()[0][3])
	nodes = []
	edges = []

	for y, x, tile in block_list:
		nodes.append(Node(x, y, tile))

	logger.end_m(__file__,inspect.stack()[0][3])
	return nodes,edges

# receives a list of positions (x,y) of platform blocks
# return nodes and edges (as tuples) representing them
def platform_to_graph(block_list):
	logger.init_m(__file__,inspect.stack()[0][3])
	from operator import itemgetter
	block_list.sort(key=itemgetter(0))
	
	nodes = []
	edges = []

	x_start = -1
	y_list, x_list, tile_list = zip(*block_list)

	for index in range(len(block_list)):
		y = y_list[index]
		x = x_list[index]
		tile = tile_list[index]
		
		if x_start == -1:
			x_start = x

			# check if there's will be a gap between current and next x
			if index+1 == len(block_list) or (index+1 < len(block_list) and x+1 < x_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y, tile)
				nodes.append(node1)
				x_start = -1

			# check if next (platform) block is of the same type as the current
			if index+1 == len(block_list) or (index+1 < len(block_list) and tile != tile_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y, tile)
				nodes.append(node1)
				x_start = -1

			# if this is the last element in the list
			# OR y is changing in the next element
			if index+1 == len(block_list) or (index+1 < len(block_list) and y != y_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y, tile)
				nodes.append(node1)
				x_start = -1

		else:
			# check if y will change in the next element
			if(index+1 < len(block_list) and y != y_list[index+1]):
				#print("Aa platform between {},{} and {},{}".format(y, x_start, y, x))	
				node1 = Node(x_start, y, tile)
				node2 = Node(x, y, tile)
				nodes.append(node1)
				nodes.append(node2)
				dist = x - x_start
				edge = (node1, node2, dist)
				edges.append(edge)
				x_start = -1
			# check if there's will be a gap between current and next x
			elif index+1 == len(block_list) or (index+1 < len(block_list) and x+1 < x_list[index+1]):
				#print("Aa platform between {},{} and {},{}".format(y, x_start, y, x))
				dist = x - x_start
				node1 = Node(x_start, y, tile)
				node2 = Node(x, y, tile)
				nodes.append(node1)
				nodes.append(node2)
				edge = (node1, node2, dist)
				edges.append(edge)
				x_start = -1
			# check if next (platform) block is of the same type as the current
			elif (index+1 < len(block_list) and tile != tile_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y, tile)
				nodes.append(node1)
				x_start = -1

	logger.end_m(__file__,inspect.stack()[0][3])
	return nodes,edges

