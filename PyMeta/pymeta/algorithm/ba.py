import numpy as np

from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin

import wx

# ref: ...
class BatAlgorithmDemo(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.A = 1  # # defaults
        self.r = 0.5
        self.Qmin = 0.0
        self.Qmax = 2
        self.name = 'Bat'
        self.npositions = 20

        self.maxstepdivisor = 100

        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user



    def search(self):
        # ## shorter names to make program easier to read
        vis = self.problem.visualiser
        f = self.problem.cost
        x = self.positions  # name x is preferred in articles
        isdraw = self.isdraw
        rand = np.random.uniform

        maxstep = (self.problem.ub - self.problem.lb) / self.maxstepdivisor

        print "hello"
        print "world"

        n = x.shape[0]  # number of particles
        d = x.shape[1]  # number of dimensions

        Q = np.zeros((n, 1))
        v = np.zeros((n, d))

        Fitness = np.array([f(pos) for pos in x])  # heights of best positions

        idx = Fitness.argmin()  # # best of the best values: global best value

        # drawing stuff
        colors = [];
        bestcolor = (1, 1, 0)
        def drawbest(pos):
            vis.drawposition(pos, color = bestcolor, scale_factor = 5)
        if self.isdraw:
            drawbest(x[idx])
            for pos in x:
                color = tuple(np.random.uniform(0, 1, (3,)).tolist())
                colors.append(color)
                vis.drawposition(pos, color = color)
                wx.Yield()  # let mlab interact with user


        # ## main loop
        bestpos = x[idx].copy()
        mincost = Fitness[idx]
        iteration = 0
        while True:
            yield (bestpos, -mincost, iteration)  # give control to caller. It will log and decide whether to stop.
            iteration = iteration + 1

            for i in xrange(n):  # #for each particle
                if isdraw:
                    wx.Yield()

                print "----------------------------"

                xi = x[i].copy(); print "xi", xi
                vi = v[i].copy(); print "vi", vi

                Q[i] = self.Qmin + (self.Qmax - self.Qmin) * rand()
                vnew = vi + (x[i] - bestpos) * Q[i]; print "vnew", vnew
                xnew = self.problem.fixbounds(xi + vnew); print "xnew", xnew

                if rand() > self.r:
                    xnew = self.problem.fixbounds(bestpos + maxstep * np.random.normal(0, 1, (d))); print "in if xnew", xnew

                print "Fitness[i]", Fitness[i]
                Fnew = f(xnew); print "Fnew", Fnew

                if (Fnew <= Fitness[i]) and (rand() < self.A):
                    x[i] = xnew.copy() ; print "better x[i] ! in if x[i]", x[i]
                    Fitness[i] = Fnew

                v[i] = x[i] - xi; print "v[i]", v[i]



                if self.isdraw:
                    vis.drawpath(xi, x[i], color = colors[i])  # draw the path

                print "============================"

                if Fnew <= mincost:
                    mincost = Fnew
                    bestpos = xnew.copy()
                    yield (bestpos, -mincost, iteration)

