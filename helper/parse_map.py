import logging
import inspect

logger = logging.getLogger(__name__)

# receives a MapMatrix object, return every occurrence of
# platform blocks as tuples (y,x)
# '#': Pyramind Block
# 'X': Ground Block
# 't': Empty Pipe
# '!': Coin Question block
# 'S': Normal Brick Block
# '?': Special Question block
# 'U': Musrhoom Brick Block
def get_platforms(map_matrix):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
	platform_blocks = ["X", '#', 't', "Q", "S", "?", "U"]
	platforms = []

	for y in reversed(range(map_matrix.y_length)):
		for x in range(len(map_matrix.map[y])):
			if map_matrix.map[y][x] in platform_blocks:
				tile_type = map_matrix.map[y][x]
				platforms.append((y, x, tile_type))

	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return platforms

# receives a MapMatrix object, return every occurrence of
# interactable blocks as tuples (y,x)
# 'g': Goomba
# 'o': Coin
def get_interactables(map_matrix):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
	interactable_blocks = ["g",  "o"]
	interactables = []

	for y in reversed(range(map_matrix.y_length)):
		for x in range(len(map_matrix.map[y])):
			if map_matrix.map[y][x] in interactable_blocks:
				tile_type = map_matrix.map[y][x]
				interactables.append((y, x, tile_type))

	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return interactables