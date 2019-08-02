from node import Node
import logging, inspect
import math
import helper.reachability as reachability	

logger = logging.getLogger(__name__)

# receives a list of positions (x,y) of interactable blocks
# return nodes and edges (as tuples) representing them
def interactable_to_graph(block_list):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
	nodes = []

	for y, x, tile in block_list:
		nodes.append(Node(x, y, tile, "C"))

	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return nodes

# receives a list of positions (x,y) of interactable blocks
# return nodes and edges (as tuples) representing them
def get_reach_edges(platforms, p_edges, interactables):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
	edges = []
	all_nodes = platforms + interactables

	for n1, n2, d, t in p_edges:
		for p in all_nodes:

			if reachability.is_reachable(n1, n2, p):
				if get_dist(n1,p) <= get_dist(n2,p):
					edge = (n1, p, get_dist(n1,p), "R")
				else:
					edge = (n2, p, get_dist(n2,p), "R")
				edges.append(edge)

	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return edges

def get_dist(node1, node2):
		dist = math.hypot(node1.x - node2.x, node2.y - node1.y)
		return dist

# run GDBScan simplified algorithm
def nodes_to_clusters(node_list, eps=4, min_pts=2):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
	def get_neighbors(node, node_list, min_dist):
		neighbors = []
		for n in node_list:
			dist = get_dist(node, n)
			if dist <= min_dist and n != node:
				neighbors.append(n)
		return neighbors

	labels = {}
	labels[-1] = {"nodes":[], "edges": []}
	processed_nodes = []
	cc = -1 # cluster counter
	
	for n in node_list:
		# if this node was processed before, ignore
		if n in processed_nodes: continue
		processed_nodes.append(n)

		neighbors = get_neighbors(n, node_list, eps)
		
		# if it has 0 neighbors, classifiy as noise
		# and continue search with next node
		if len(neighbors) < min_pts:
			labels[-1]["nodes"].append(n)
			continue

		cc += 1
		labels[cc] = {"nodes":[n], "edges": []}

		# process the neighbors
		for neighbor in neighbors:
			print("processing neighbor ", neighbor)
			if neighbor in processed_nodes:
				if neighbor in labels[-1]["nodes"]:
					labels[-1]["nodes"].remove(neighbor)
					labels[cc]["nodes"].append(neighbor)
				else: 
					continue

			labels[cc]["nodes"].append(neighbor)
			edge = (n, neighbor, get_dist(n,neighbor), "C")
			labels[cc]["edges"].append(edge)
			processed_nodes.append(neighbor)

			neighbors_of_neighbor = get_neighbors(neighbor, node_list, eps)
			for n_of_n in neighbors_of_neighbor:
				if n_of_n not in neighbors:
					neighbors.append(n_of_n)

	for key, value in labels.items():
		print("Cluster: {}, Node: {}".format(key,value))
	
	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return labels


# receives a list of positions (x,y) of platform blocks
# return nodes and edges (as tuples) representing them
def platform_to_graph(block_list):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
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
				edge = (node1, node2, dist, "P")
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
				edge = (node1, node2, dist, "P")
				edges.append(edge)
				x_start = -1
			# check if next (platform) block is of the same type as the current
			elif (index+1 < len(block_list) and tile != tile_list[index+1]):
				#print("An isolated block at {},{}".format(y, x))
				node1 = Node(x, y, tile)
				nodes.append(node1)
				x_start = -1

	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return nodes,edges

