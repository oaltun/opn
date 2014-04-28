import numpy as np
#from numpy import *
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm

# recombine solution with index i, with a random other solution in the
# population x. return new solution and its
def abc_recombination(i, x):
    #get a mate
    while True:
        j = np.random.randint(len(x))
        if not(i == j): break

    #get a dim
    d = np.random.randint(len(x[0]))

    xtmp = x[i].copy()
    xtmp[d] = x[i][d] + (x[i][d] - x[j][d]) * np.random.uniform(-1, 1)
    return xtmp


# TODO: this is a bad approach. there is a big difference between
# 0.000001 and -0.99999. Try something different
def assignprobabilities(fx):
    fit = fx.copy()
    for i, e in enumerate(fit):
        if e >= 0:
            fit[i] = e + 1
        else:
            fit[i] = 1.0 / (1 - e)
    return 0.9 * fit / float(np.max(fit)) + 0.1

#ref Essentials of Metaheuristics, by Sean Luke
class ArtificialBeeColony(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.maxstepdivisor = 70
        self.name = 'ABC'
        self.npositions = 50

        self.limit = 100  # when to leave food sources
        self.crossover = lambda i, x: abc_recombination(i, x)

        self.__dict__.update(**kwargs)  # overwrite
        self.minimize = False

    def search(self):

        #### sugar
        randomrecombine = self.crossover
        f = self.f
        r = np.random.uniform
        fx = self.fx

        #### main loop
        trial = np.zeros_like(fx)
        while True:  #for each generation
            yield

            # re-visit all sources (employed bee phase)
            for i, e in enumerate(self.x):
                xnew, fnew = f(randomrecombine(i, self.x)); yield
                if fnew >= fx[i]:
                    self.updatex(xnew, fnew, i)
                    trial[i] = 0
                else:
                    trial[i] += 1

            ## re visit good sources (onlooker bee phase)
            # assign re-visit probability
            prob = assignprobabilities(fx)
            for i, e in enumerate(prob):
                if e > r():
                    xnew, fnew = f(randomrecombine(i, self.x)); yield
                    if fnew >= fx[i]:
                        self.updatex(xnew, fnew, i)
                        trial[i] = 0
                    else:
                        trial[i] += 1

            # leave inactive sources (scout phase)
            for i, e in enumerate(trial):
                if e >= self.limit:
                    xnew, fnew = f(self.problem.randpos()); yield
                    trial[i] = 0
                    self.updatex(xnew, fnew, i, False)  # do not draw path

                    #assign a new color, as old path is abandoned
                    if self.isdraw:
                        self._poscolors[i] = (r(), r(), r())
