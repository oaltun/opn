import numpy as np
#from numpy import *
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm


#tournament selection. ref: Essentials of metaheuristics.
#fp: fitnesses of the population. t: tournament size, t>=1
def tournament_selection(fp, t):
    n = fp.shape[0]
    best = np.random.randint(n)
    for _ in range(2, t + 1):
        nxt = np.random.randint(n)
        if fp[nxt] > fp[best]:
            best = nxt
    return best

# intermediate recombination from Essentials of metaheuristics by Sean Luke.
# vectorised. no bounds checking, that is done automatically in pymeta.
def intermediate_recombination(v, w, p):
    a = np.random.uniform(-p, 1 + p, v.shape)
    b = np.random.uniform(-p, 1 + p, v.shape)
    t = a * v + (1 - a) * w
    s = b * w + (1 - b) * v
    return t, s

#ref Essentials of Metaheuristics, by Sean Luke
class GeneticAlgorithm(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.maxstepdivisor = 70
        self.name = 'GA'
        self.npositions = 5
        self.p = 0.25  # for intermediate recombination
        self.t = 2     # for tournament selection

        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user

        self.minimize = False
        self.select = lambda fp: tournament_selection(fp, self.t)
        self.crossover = lambda v, w: intermediate_recombination(v, w, self.p)

# def return_ts(self, fp):
#     return tournament_selection( fp,self.t)
# 
# self.select = return_ts

    def search(self):

        #### sugar
        select = self.select
        crossover = self.crossover
        def mutate(sol):
            xtmp = self.problem.tweak(sol)
            xnew, fnew = self.f(xtmp)
            if np.array_equal(xnew, sol):
                raise Exception('whaat tweak gave same value???')
            return xnew, fnew

        while True:  #for each generation
            yield

            #### get next generation q
            q = np.empty_like(self.x)
            fq = np.empty_like(self.fx)
            iq = 0
            nq = q.shape[0]
            while iq < nq:  #reproduction loop
                yield
                pa = select(self.fx)  #obtain parent 1
                pb = select(self.fx)  #obtain parent 2
                ca, cb = crossover(self.x[pa], self.x[pb])  #crossover
                for c in (ca, cb):
                    if iq < nq:
                        a, fa = mutate(c);yield  #mutate
                        q[iq] = a
                        fq[iq] = fa
                        iq += 1

            #### copy next generation q over current generation x.
            for i, e in enumerate(q):
                self.updatex(e, fq[i], i)
















