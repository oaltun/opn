#reference: Essentials of Metaheuristics, First Edition (Rev C) Online Version 1.3, February, 2012 by Sean Luke, Section 11.2.2
from numpy import *
from pymeta.problem.problembase import GenericOptimizationProblem
#from pymeta.visualiser.funvis import TwoDFunVisualiser

class NegativeRastriginProblem(GenericOptimizationProblem):
	"""Rastrigin Problem (for maximization)"""
	ub =None
	lb =None
	name = None
	
	def __init__(self, dim=2, bound=5.12):
		self.ub = bound * ones(dim)
		self.lb = -1 * self.ub
		self.name='Negative Rastrigin Problem'
		#self.visualiser = TwoDFunVisualiser(fun=self.height,lb=self.lb,ub=self.ub,(self.ub-self.lb)/100)
	def height(self, x):
		r = 10*size(x) + sum(x*x - 10*cos(2*pi*x))
		return -r #maximization
	
	