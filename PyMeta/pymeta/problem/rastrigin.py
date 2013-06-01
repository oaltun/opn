#reference: Essentials of Metaheuristics, First Edition (Rev C) Online Version 1.3, February, 2012 by Sean Luke, Section 11.2.2
from pymeta.problem.problembase import GenericOptimizationProblem
from pymeta.visualiser.funvis import TwoDFunVisualiser

#numpy must overwrite all
from numpy import *

class NegativeRastriginProblem(GenericOptimizationProblem):
	def __init__(self, **kwargs):
		GenericOptimizationProblem.__init__(self)
		self.ub = array([5.12,5.12])
		self.lb = -1 * self.ub
		self.name='NRP'
		self.visualiser = TwoDFunVisualiser(fun=self.height,lb=self.lb,ub=self.ub,step=(self.ub-self.lb)/100)
		self.heightfun = lambda x: -1*(10*size(x) + sum(x*x - 10*cos(2*pi*x)))
		self.__dict__.update(**kwargs)
	
# 	def heightfun(self,x):
# 		return -1*(10*size(x) + sum(x*x - 10*cos(2*pi*x)))