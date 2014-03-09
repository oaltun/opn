# reference: Essentials of Metaheuristics, First Edition (Rev C)
# Online Version 1.3, February, 2012 by Sean Luke, Section 11.2.2
from pymeta.problem.problembase import GenericOptimizationProblem
from pymeta.visualiser.funvis import TwoDFunVisualiser
import pymeta as pm
import numpy as np
from pymeta import dprint

# numpy must overwrite all
from numpy import *

class NegativeRastriginProblem(GenericOptimizationProblem):
    def __init__(self, **kwargs):
        GenericOptimizationProblem.__init__(self)  # inherit

        self.ub = array([5.12, 5.12])  # #defaults
        self.lb = -1 * self.ub
        self.name = 'RastriginNeg'
        self.minimize = False
        self.optimum = 0.0
        self.optimumsol = np.zeros_like(self.ub)
        self.visualiser = TwoDFunVisualiser(fun = self.heightfun, lb = self.lb,
                         ub = self.ub, step = (self.ub - self.lb) / 100)
        # self.heightfun = lambda x: -1*(10*size(x) + sum(x*x - 10*cos(2*pi*x)))
        self.__dict__.update(**kwargs)  # #overwrite

    def heightfun(self, x):
        return -1 * (10 * size(x) + sum(x * x - 10 * cos(2 * pi * x)))

class RastriginProblem(GenericOptimizationProblem):
    def __init__(self, **kwargs):
        dprint('RastriginProblem.__init__')
        GenericOptimizationProblem.__init__(self)  # inherit

        self.ub = array([5.12, 5.12])  # #defaults
        self.lb = -1 * self.ub
        self.name = 'Rastrigin'
        self.optimum = 0.0  #theorical optimal value
        self.visualiser = TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
             ub = self.ub, step = (self.ub - self.lb) / 100)
        # self.heightfun = lambda x: -1*(10*size(x) + sum(x*x - 10*cos(2*pi*x)))
        self.__dict__.update(**kwargs)  # #overwrite
        self.minimize = True

    def costfun(self, x):
        return 10 * size(x) + sum(x * x - 10 * cos(2 * pi * x))
