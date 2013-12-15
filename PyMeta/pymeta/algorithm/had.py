
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin

# HillClimbing:
class HillAscend(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'ha'
        self.minimize = False  # if True, assume the problem is to be minimized by this algorithm.
        self.maxstepdivisor = 40

        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user

    def search(self):

        # ## main loop
        while True:  # for each time step (generation)
            for i in xrange(self.n):  # #for each climber i
                yield
                # ## peek: take a look to a close to this position: xtmp
                xtmp = self.x[i] + randin(-self.maxstep, self.maxstep)
                xnew, fnew = self.f(xtmp)
                if self.isbetter(fnew, self.fx[i]):
                    self.updatex(xnew, fnew, i)



class HillDescend(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'hd'
        self.minimize = True  # if True, assume the problem is to be minimized by this algorithm.
        self.maxstepdivisor = 40

        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user

    def search(self):

        # ## main loop
        while True:  # forever...
            for i in xrange(self.n):  # #for each climber i
                yield  # let the controller decide whether stop or continue.
                # ## peek: take a look to a close to this position: xtmp
                xtmp = self.x[i] + randin(-self.maxstep, self.maxstep)
                xnew, fnew = self.f(xtmp)
                if self.isbetter(fnew, self.fx[i]):
                    self.updatex(xnew, fnew, i)






