import numpy as np
#from numpy import *
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm

# based on intermediate recombination from Essentials of metaheuristics
# by Sean Luke. vectorised. no bounds checking, that is done automatically
# in self.f()
def intermediate_recombination_single_child(v, w, p):
    a = np.random.uniform(-p, 1 + p, v.shape)
    r = a * v + (1 - a) * w
    return r

def random_except(length, tabulist):
    while True:
        r = np.random.randint(length)
        if not (r in tabulist): break
    return r

#ref Essentials of Metaheuristics, by Sean Luke
class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.maxstepdivisor = 70
        self.name = 'DE'
        self.npositions = 50
        self.p = 0.25  # for intermediate recombination
        self.mutationrate = 0.75

        self.__dict__.update(**kwargs)  # overwrite defaults

        self.minimize = False
        self.crossover = lambda v, w: \
            intermediate_recombination_single_child(v, w, self.p)

    def search(self):

        while True:  # for each generation
            yield
            q = self.x.copy()  # parents
            nq = q.shape[0]
            for i, e in enumerate(q):  # let parent have a child
                ia = random_except(nq, (i,))
                ib = random_except(nq, (i, ia))
                ic = random_except(nq, (i, ia, ib))
                d = q[ia] + self.mutationrate * (q[ib] - q[ic])
                child = self.crossover(d, e)
                xnew, fnew = self.f(child); yield
                if fnew >= self.fx[i]:  # accept child if it exceeds its parent
                    self.updatex(xnew, fnew, i)

