#reference: Essentials of Metaheuristics, First Edition (Rev C) Online Version 1.3, February, 2012 by Sean Luke, Section 11.2.2
from numpy import *

class NegativeRastriginProblem:
	"""Rastrigin Problem (for maximization)"""
	
	def __init__(self, dim=2, bound=5.12):
		self.ub = bound * ones(dim)
		self.lb = -1 * self.ub
		
	def height(self, x):
		r = 10*size(x) + sum(x*x - 10*cos(2*pi*x))
		return -r #maximization
	
	