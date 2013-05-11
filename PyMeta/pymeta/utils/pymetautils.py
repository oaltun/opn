from numpy import *
import numpy as np


def randin(lb,ub):
	"""return random array with elements between the elements of lb and ub. ub is not included."""
	r=(ub-lb)*random.random(shape(lb)) + lb
	if r[0] is np.NAN:
		print 'r is non'
	return r
	
	
	

class Default:
	pass
# 	def __init__(self, **kwargs):
# 		self.__dict__.update(**kwargs)
		
# 	def __getattr__(self, attr):
# 		return self.__dict__.get(attr, None)
	
# 	def __repr__(self):
# 		keys = [key for key in dir(self) if not key.startswith('_')]
# 		return 'dict:'+str(self.__dict__)+'keys:'+str(keys)


				
		

# class Struct(Default):
# 	"""Class that can be used similar to a matlab struct"""
# 	pass