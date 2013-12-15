#from numpy import *
import numpy as np


def randin(lb, ub):
	"""return random array with elements between the elements of
	lb and ub. ub is not included."""

	r = (ub - lb) * np.random.random(np.shape(lb)) + lb
	if r[0] is np.NAN:
		print 'r is non'
	return r


def dict_configure(orig, **options):
	""" overwrite already-existing/default values in the original
	dictionary with the ones in the options dictionary.
	if the options dictionary has keys that are not in orig, they
	are not assigned to orig. This function is intended for
	easy, safe option assignments in places like __init__()
	functions"""

	for key in orig:
		if key in options:
			orig[key] = options[key]


class Default:
	def __init__(self):
		pass

	def configure(self, **options):
		""" overwrite already-existing / default values in the
		self.dict with the values in options"""

		dict_configure(self.dict, **options)



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


if __name__ == '__main__':
	d = Default
	d.dict['a'] = 1

