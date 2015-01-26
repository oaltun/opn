# reference: Essentials of Metaheuristics, First Edition (Rev C) Online Version
# 1.3, February, 2012 by Sean Luke, Section 11.2.2

import opn as pm
import numpy as np

# TODO: get rid of this "from numpy import *"
from numpy import *

# TODO: get rid of "self.visualiser = ..." lines.
#     visualiser must be attached by the user 

# TODO: simplify problem objects to subclass and use "RealValuedFunctionProblem"
class RealValuedFunctionProblem(pm.OptimizationProblem):
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self, **kwargs)
        self.ub = array([5.12, 5.12])
        self.lb = -1 * self.ub
        self.minimize = True
        self.visualiser = pm.TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)

class SphereProblem(pm.OptimizationProblem):
    ''' Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    Online Version 2.0, June 2013'''
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([5.12, 5.12])  # #defaults
        self.lb = -1 * self.ub
        self.name = 'Sphere'
        self.optimum = 0.0
        self.optimumsol = np.zeros_like(self.ub)
        self.visualiser = pm.TwoDFunVisualiser(fun = self.cost, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite
        self.minimize = True

    def costfun(self, x):
        return sum(x * x)

class RastriginProblem(pm.OptimizationProblem):
    ''' Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    Online Version 2.0, June 2013'''
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([5.12, 5.12])  # #defaults
        self.lb = -1 * self.ub
        self.name = 'Rastrigin'
        self.optimum = 0.0
        self.optimumsol = np.zeros_like(self.ub)
        self.visualiser = pm.TwoDFunVisualiser(fun = self.cost, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite
        self.minimize = True

    def costfun(self, x):
        return 10*x.size + sum(x * x - 10 * cos(2 * pi * x))

class RosenbrockProblem(pm.OptimizationProblem):
    ''' Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    Online Version 2.0, June 2013'''
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([2.048, 2.048])  # #defaults
        self.lb = -1 * self.ub
        self.name = 'Rosenbrock'
        self.minimize = True
        self.visualiser = pm.TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite

    def costfun(self, x):
        return sum((1 - x[:-1]) ** 2.0 + 100.0 *
                   (x[1:] - x[:-1] ** 2.0) ** 2.0)

class AckleyProblem(pm.OptimizationProblem):
    ''' Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    Online Version 2.0, June 2013'''
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([30, 30])  # #defaults
        self.lb = array([-15, -15])
        self.name = 'Ackley'
        self.minimize = True
        self.visualiser = pm.TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite

    def costfun(self, x):
        return (-20.0 * exp(-0.2 * sqrt(sum(x * x) / size(x))) -
                exp(sum(cos(2.0 * pi * x)) / size(x)) + 20 + e)

class SumProblem(pm.OptimizationProblem):
    ## Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    ## Online Version 2.0, June 2013
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([1, 1])  # #defaults
        self.lb = array([0, 0])
        self.name = 'Sum'
        self.minimize = True
        self.visualiser = pm.TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite

    def costfun(self, x):
        return sum(x)

class StepProblem(pm.OptimizationProblem):
    ## Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    ## Online Version 2.0, June 2013
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([5.12, 5.12])  # #defaults
        self.lb = -1 * self.ub
        self.name = 'Step'
        self.minimize = True
        self.visualiser = pm.TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite

    def costfun(self, x):
        return 6.0 * size(x) + sum(abs(x))

class SchwefelProblem(pm.OptimizationProblem):
    ## Ref : Essentials of Metaheuristics, Sean Luke, Second Edition,
    ## Online Version 2.0, June 2013
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = array([511.97, 511.97])  # #defaults
        self.lb = -1 * array([512.03, 512.03])
        self.name = 'Schwefel'
        self.minimize = True
        self.visualiser = pm.TwoDFunVisualiser(fun = self.costfun, lb = self.lb,
            ub = self.ub, step = (self.ub - self.lb) / 100.0)
        self.__dict__.update(**kwargs)  # #overwrite

    def costfun(self, x):
        return sum(-x * sin(sqrt(abs(x))))
