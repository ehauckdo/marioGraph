import logging, inspect
logger = logging.getLogger(__name__)

def is_reachable(p1, p2, n, dist=5):
	logger.debug(" (CALL) {}".format(inspect.stack()[0][3]))
	
	def area(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
		return abs((p1_x*(p2_y-p3_y) + p2_x*(p3_y-p1_y) 
										+ p3_x*(p1_y-p2_y))/2.0)

	def inside_triangle(n1, n2, dist):
		p1_x = n1.x - dist 
		p1_y = n1.y
		p2_x = n1.x + dist
		p2_y = n1.y
		p3_x = n1.x
		p3_y = n1.y - dist

		A = area(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y)
		A1 = area(n2.x, n2.y, p2_x, p2_y, p3_x, p3_y)
		A2 = area(p1_x, p1_y, n2.x, n2.y, p3_x, p3_y)
		A3 = area(p1_x, p1_y, p2_x, p2_y, n2.x, n2.y)
		return abs(A1 + A2 + A3 - A) <= 0.001

	def inside_rectangle(n1, n2, n3, dist):
		top = n1.y - dist
		bottom = n1.y
		left = n1.x
		right = n2.x
		if n3.x >= left and n3.x <= right and n3.y <= bottom and n3.y >= top:
			return True
		else: return False

	is_inside = inside_triangle(p1, n, dist) or inside_triangle(p2,n,dist) or inside_rectangle(p1, p2, n, dist)
	logger.debug(" (RTRN) {}".format(inspect.stack()[0][3]))
	return is_inside