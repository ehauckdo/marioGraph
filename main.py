# TEMPORARY MAIN FILE
import sys
import optparse
import logging
import networkx as nx
from node import Node
import helper.map_to_graph as map_to_graph
import helper.parse_map as parse_map
from map_matrix import MapMatrix
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.DEBUG)

def get_graph(map_matrix):
	nodes = []
	edges = []

	# fetch plaftorms
	platforms = parse_map.get_platforms(map_matrix)
	platform_nodes,platform_edges = map_to_graph.platform_to_graph(platforms)
	nodes.extend(platform_nodes)
	edges.extend(platform_edges)

	# fetch interactables
	interactables = parse_map.get_interactables(map_matrix)
	interactable_nodes, interactable_edges = map_to_graph.interactable_to_graph(interactables)
	nodes.extend(interactable_nodes)
	edges.extend(interactable_edges)

	map_to_graph.nodes_to_clusters(interactable_nodes)

	# initialize networkx graph
	G = nx.Graph()
	for n in nodes:
		G.add_node(n, pos=(n.x, n.y), tile=n.tile, type=n.type)
	for n1,n2,d in edges:
		G.add_edge(n1,n2)
		attr = {(n1, n2): {'dist':d}}
		nx.set_edge_attributes(G, attr)
	
	logging.info("Number of nodes: {}".format(G.number_of_nodes()))
	logging.info("Number of edges: {}".format(G.number_of_edges()))

	# this will give the plot inverted, because it's a regular x,y axis
	pos = nx.get_node_attributes(G,'pos')
	# this will give the plot like in the game, with y increasing downwards
	flipped_pos = {node: (x,-y) for (node, (x,y)) in pos.items()}

	nx.draw(G, flipped_pos)

	# add labels to nodes
	node_labels = nx.get_node_attributes(G,'type')
	nx.draw_networkx_labels(G, flipped_pos, labels = node_labels,font_size=7)

	# add labels to edges
	edge_labels = nx.get_edge_attributes(G,'dist')
	nx.draw_networkx_edge_labels(G, flipped_pos, labels = edge_labels, font_size=7)

	plt.show()


def parseArgs(args):
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage=usage) 

	parser.add_option('-m', action="store", type="string", dest="mapfile",help="Path/name of the map file", default="maps/map1-1.txt")

	(opt, args) = parser.parse_args()
	return opt, args

if __name__ == '__main__':
	opt, args = parseArgs(sys.argv[1:])
	print(opt.mapfile)

	map_matrix = MapMatrix(opt.mapfile)
	#map_matrix.print_map()
	
	get_graph(map_matrix)

	G = nx.Graph()