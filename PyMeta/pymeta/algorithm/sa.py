
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin
from pymeta import dprint
import numpy as np

# HillClimbing:
class SimulatedAnnealingRandomRestart(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.name = 'SARR'
        self.maxstepdivisor = 40
        self.limit = 8
        self.t0 = 100.0  #initial temperature
        self.cooler = .9  #cooling factor
        # overwrite defaults with keyword arguments supplied by user
        self.overwrite(**kwargs)

        self.minimize = True
        self.npositions = 1

    def search(self):
        while True:  # for each restart
            yield

            #reset color
            if self.isdraw:
                self.poscolors[0] = (np.random.uniform(),
                                    np.random.uniform(),
                                    np.random.uniform())

            #reset temperature
            t = self.t0

            ## get a new random starting x
            xtmp = self.problem.randpos()
            xnew, fnew = self.f(xtmp)
            self.updatex(xnew, fnew, 0)


            ## tweak the point until we get self.limit unsuccessful
            ## trials
            badtrial = 0
            while badtrial < self.limit:
                xold = xnew.copy()
                xtmp = self.problem.tweak(xnew)
                xnew, fnew = self.f(xtmp);yield

                if np.array_equal(xold, xnew):
                    raise Exception('whaat tweak gave same value???')


                if (fnew < self.fx[0] or
                    np.random.uniform(0, 1) < np.exp((self.fx[0] - fnew) / t)):
                    self.updatex(xnew, fnew, 0)
                    badtrial = 0
                else:
                    badtrial += 1

                #decrease t
                t *= self.cooler

