from node import Node
import logger
import logging
import inspect	

def get_platforms(map_matrix):
	logger.init_m(__file__,inspect.stack()[0][3])
	platform_blocks = ["X"]
	platforms = []

	for y in reversed(range(map_matrix.y_length)):
		for x in range(len(map_matrix.map[y])):
			if map_matrix.map[y][x] in platform_blocks:
				platforms.append((y, x))

	logger.end_m(__file__,inspect.stack()[0][3])
	return platforms

def platform_to_graph(block_list):
	logger.init_m(__file__,inspect.stack()[0][3])
	from operator import itemgetter
	block_list.sort(key=itemgetter(0))
	
	nodes = []
	edges = []

	x_start = -1
	y_list, x_list = zip(*block_list)

	for index in range(len(block_list)):
		y = y_list[index]
		x = x_list[index]
		
		if x_start == -1:
			x_start = x

			# check if there's will be a gap between current and next x
			if index+1 == len(block_list) or (index+1 < len(block_list) and x+1 < x_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y)
				nodes.append(node1)
				x_start = -1

			# if this is the last element in the list
			# OR y is changing in the next element
			if index+1 == len(block_list) or (index+1 < len(block_list) and y != y_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y)
				nodes.append(node1)
				x_start = -1

		else:
			# check if y will change in the next element
			if(index+1 < len(block_list) and y != y_list[index+1]):
				#print("Aa platform between {},{} and {},{}".format(y, x_start, y, x))	
				node1 = Node(x_start, y)
				node2 = Node(x, y)
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
				node1 = Node(x_start, y)
				node2 = Node(x, y)
				nodes.append(node1)
				nodes.append(node2)
				edge = (node1, node2, dist)
				edges.append(edge)
				x_start = -1

	logger.end_m(__file__,inspect.stack()[0][3])
	return nodes,edges

