from numpy import *


def randin(lb,ub):
	"""return random array with elements between the elements of lb and ub. ub is not included."""
	return (ub-lb)*random.random(shape(lb)) + lb
	
