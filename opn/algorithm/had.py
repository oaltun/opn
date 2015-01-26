
import numpy as np
import opn as pm


class RandomSearch(pm.OptimizationAlgorithm):
    """
    Simplest blind random search metaheuristics.
    Just check random positions till termination.
    """

    def __init__(self, **kwargs):
        # inherit
        pm.OptimizationAlgorithm.__init__(self)

        self.name = 'rs'

        # overwrite defaults with keyword arguments
        # supplied by user
        self.__dict__.update(**kwargs)
        self.npositions = 1
        #assume this is a minimization algorithm.
        self.minimize = True

    def search(self):
        while True:
            yield
            self.f(self.problem.randpos())


class HillClimbingParallel(pm.OptimizationAlgorithm):
    def __init__(self, **kwargs):
        pm.OptimizationAlgorithm.__init__(self)  # inherit

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
                xtmp = self.x[i] + pm.randin(-self.maxstep, self.maxstep)
                xnew, fnew = self.f(xtmp)
                if self.isbetterORequal(fnew, self.fx[i]):
                    self.updatex(xnew, fnew, i)

# other names for backward compatibility
ParallelClimbing = HillClimbing = HillAscend = HillClimbingParallel


class HillClimbingRandomRestart(pm.OptimizationAlgorithm):
    def __init__(self, **kwargs):
        pm.OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'hars'
        self.maxstepdivisor = 40
        self.limit = 100
        self.isdrawupdatex=True

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

            ## climb the point until we get self.limit unsuccessful trials to
            ## climb
            badtrial = 0
            while badtrial < self.limit:
                xold = xnew.copy()
                xtmp = self.problem.tweak(xnew)
                xnew, fnew = self.f(xtmp)

                if np.array_equal(xold, xnew):
                    raise Exception('whaat tweak gave same value???')

                if fnew > self.fx[0]:
                    self.updatex(xnew, fnew, 0)
                    badtrial = 0
                else:
                    badtrial += 1
                    
# Additional name for backward compatibility:
HillAscendRandomRestart = HillClimbingRandomRestart
