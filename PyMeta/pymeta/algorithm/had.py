
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin
from pymeta import dprint
import numpy as np

# HillClimbing:
class HillAscend(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'ha'
        self.maxstepdivisor = 40

        # overwrite defaults with keyword arguments supplied by user
        self.__dict__.update(**kwargs)

        # if True, assume the problem is to be minimized by this algorithm.
        self.minimize = False

    def search(self):

        # ## main loop
        while True:  # for each time step (generation)
            for i in xrange(self.n):  # #for each climber i
                yield
                # ## peek: take a look to a close to this position: xtmp
                xtmp = self.x[i] + randin(-self.maxstep, self.maxstep)
                xnew, fnew = self.f(xtmp)
                if self.isbetterORequal(fnew, self.fx[i]):
                    self.updatex(xnew, fnew, i)


# HillClimbing:
class HillAscendRandomRestart(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'hars'
        self.maxstepdivisor = 40
        self.limit = 100

        # overwrite defaults with keyword arguments supplied by user
        self.overwrite(**kwargs)

        self.minimize = False
        self.npositions = 1

    def search(self):
        while True:  # for each restart
            yield
            ## get a new random starting x
            xtmp = self.problem.randpos()
            xnew, fnew = self.f(xtmp)
            self.updatex(xnew, fnew, 0)

            ## climb the point until we get self.limit unsudcessful trials to
            ## climb
            badtrial = 0
            while badtrial < self.limit:
                xold = xnew.copy()
                xtmp = self.problem.tweak(xnew)
                xnew, fnew = self.f(xtmp)

                if np.array_equal(xold, xnew):
                    raise Exception('whaat tweak gave same value???')

                if self.isbetterORequal(fnew, self.fx[0]):
                    self.updatex(xnew, fnew, 0)
                    badtrial = 0
                else:
                    badtrial += 1




class HillDescend(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'hd'
        self.maxstepdivisor = 40

        self.__dict__.update(**kwargs)

        self.minimize = True

    def search(self):

        # ## main loop
        while True:  # forever...
            for i in xrange(self.n):  # #for each climber i
                yield  # let the controller decide whether stop or continue.
                # ## peek: take a look to a close to this position: xtmp
                xtmp = self.x[i] + randin(-self.maxstep, self.maxstep)
                xnew, fnew = self.f(xtmp)
                if self.isbetterORequal(fnew, self.fx[i]):
                    self.updatex(xnew, fnew, i)









