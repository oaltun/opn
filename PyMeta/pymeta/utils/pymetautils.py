#from numpy import *
import numpy as np
import os
import collections

def randin(lb, ub):
	"""return random array with elements between the
	elements of lb and ub. ub is not included."""

	r = ((ub - lb) * np.random.random(np.shape(lb))
        + lb)
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

import random
import random
import numpy as np
from random import randint
import numbers

def randdiv(amount, cnt):
	"""Divides the AMOUNT into CNT random parts and returns those
	parts in a numpy array. CNT must not be bigger than AMOUNT.
	Both CNT and AMOUNT must be integers.

	>>> random.seed(0)
	>>> randdiv(100,10)
	array([ 5,  6,  9,  8, 11, 15,  8,  9, 17, 12])

	"""

	def argcheck(amount, cnt):
		if cnt > amount:
			raise Exception('cnt should be bigger or equal to amount')
		if not isinstance(amount, numbers.Integral):
			raise Exception('amount must be int')
		if not isinstance(cnt, numbers.Integral):
			raise Exception('cnt must be int')

	argcheck(amount, cnt)

	div = np.ones((cnt), dtype = int)
	rem = amount - cnt

	while rem > 0:
		div[random.randrange(0, cnt)] += 1
		rem -= 1
	return div

class Table:
	def __init__(self):

		self.default_alignment = 'C'
		self.width = '\\linewidth'
		self.header_escape = {'#': '\#'}
		self.order = collections.OrderedDict()  #TODO: make self.order readonly (by using property decorator?)
		self.table = []

	def row(self):
		self.table.append({})

	def add(self, col, content, **kwargs):
		self.order[col] = 1
		self.table[-1][col] = dict(name = col, content = content, **kwargs)

	def latex_data(self, fid):
		'''fid: file or similar. E.g. file or StringIO or ... any object that defines a proper write() method.'''
		for irow in range(len(self.table)):
			lst = []
			for colname in self.order:
				content = self.table[irow][colname]['content']
				content = str(content)
				lst.append(content)
			fid.write(' & '.join(lst) + '\\\\\n')

	def latex_header(self, fid):
		fid.write(' & '.join((self.hesc(key) for key in self.order.keys())) + '\\\\\n')

	def latex_alignments_tabulary(self, fid):
		lst = []
		for colname in self.order:
			if 'align' in self.table[0][colname]:
				lst.append(self.table[0][colname]['align'])
			else:
				lst.append(self.default_alignment)
		fid.write('{' + ''.join(lst) + '}')

	def latex_tabulary(self, fid):
		fid.write('\\begin{tabulary}{%s}' % self.width)
		self.latex_alignments_tabulary(fid)
		fid.write('\\hline\n')
		self.latex_header(fid)
		fid.write('\\hline\n')
		self.latex_data(fid)
		fid.write('\\hline\n')
		fid.write('\\end{tabulary}\n')


	def dlt(self, astr):
		astr = astr.replace('[', '')
		astr = astr.replace(']', '')

	def hesc(self, astr):
		"""escape special characters like #"""
		for key in self.header_escape:
			astr = astr.replace(key, self.header_escape[key])
		return astr



if __name__ == '__main__':
	pass
