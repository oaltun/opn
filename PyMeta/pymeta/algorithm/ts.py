
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin
from pymeta import dprint
import numpy as np
import collections

#check whether deque d has a copy of numpy array a
def deque_has(d, a):
    for e in d:
        if np.array_equal(e, a):
            return True
    return False

#check whether deque d has any element e closer than threshold t to array a
def deque_similar(d, a, t):
    for e in d:
        if np.linalg.norm(e - a) < t:
            return True
    return False

# Ref: Essentials of Metaheuristics, by Sean Luke
class TabuSearch(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'TS'
        self.maxstepdivisor = 10
        self.tabulen = 100  #desired maximum tabu list length
        self.nt = 8  #number of tweaks desired to sample the gradient

        self.real = True  # if true, position values are real. not discreet.
        self.tabudistdivisor = 100;

        # overwrite defaults with keyword arguments supplied by user
        self.overwrite(**kwargs)

        self.minimize = False  # assume the algorithm is maximizing
        self.npositions = 1

        self.tabulist = collections.deque(maxlen = self.tabulen)
        self.tabu = lambda a: deque_has(self.tabulist, a)



    def search(self):

            #### setup for real mode if necessary
            if self.real:
                self.tabudist = \
                    np.linalg.norm(self.problem.lb - self.problem.ub) \
                    / float(self.tabudistdivisor)
                self.tabu = lambda a: deque_similar(self.tabulist, a, self.tabudist)

            #### sugar
            tabu = self.tabu
            def mytweak(sol):
                xtmp = self.problem.tweak(sol)
                xnew, fnew = self.f(xtmp)
                if np.array_equal(xnew, sol):
                    raise Exception('whaat tweak gave same value???')
                return xnew, fnew

        #while True:  # for each restart
            yield

#            #reset color
#            self._poscolors[0] = (np.random.uniform(),
#                                np.random.uniform(),
#                                np.random.uniform())

            ## some initial candidate solution
            xtmp = self.problem.randpos()
            S, fS = self.f(xtmp)  # S
            self.updatex(S, fS, 0, False)

            self.tabulist.append(S)


            while True:
                yield

                ### sample the gradient
                R, fR = mytweak(S)
                for _ in range(1, self.nt):
                    W, fW = mytweak(S)
                    if not(tabu(W)) and (fW > fR or tabu(R)):
                        R = W
                        fR = fW

                ### update S if necessary
                if not(tabu(R)) and fR > fS:
                    S = R
                    fS = fR
                    self.updatex(S, fS, 0, True)
                    self.tabulist.append(R)

