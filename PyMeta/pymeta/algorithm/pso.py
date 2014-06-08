import numpy as np
import wx

from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin


#___________________________________________________________________
# ref: wikipedia.com/Particle_swarm_optimization
class ParticleSwarmOptimization(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.w = 0.90  # intertia weight
        self.psip = 0.10  #cognitive parameter
        self.psig = 0.60  #social parameter
        self.conf = 1.0  #constriction factor
        self.maxstepdivisor = 70
        self.name = 'PSO'
        self.npositions = 20

        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user

        self.minimize = False

    def search(self):

        v = np.array([randin(-self.maxstep, self.maxstep) for _ in xrange(self.n)])  # initial velocities of the particles
        p = self.x.copy()  # best known position of each particle. make a hard copy of x
        fp = self.fx.copy()


        # ## main loop
        while True:
            print '1'
            for i in xrange(self.n):  # #for each particle
                yield  # give control to caller. It will log and decide whether to stop.

                # ## old values
                xo = self.x[i].copy()
                vo = v[i].copy()
                po = p[i].copy()

                rp = np.random.uniform(0, 1)  # # produce a new position
                rg = np.random.uniform(0, 1)
                # new velocity
                # TODO: restart randomly when po-xo is very close to xbest-xo. Or xnew is too close to xbest
                vtmp = self.conf * (vo * self.w + (po - xo) * rp * self.psip + (self.xbest - xo) * rg * self.psig)
                #xtmp = xo + vtmp
                xtmp = self.problem.stepby(xo, vtmp)

                xnew, fnew = self.f(xtmp); yield  # correct position, compute its f, and update self.fbest and self.xbest
                self.updatex(xnew, fnew, i)
                print 2, self.problem.assessmentcnt()

                v[i] = xnew - xo  # correct velocity

                if fnew > fp[i]:  # # update personal best
                    print 3
                    self.drawpersonalbestpath(p[i], xnew, i)
                    p[i] = xnew.copy()
                    fp[i] = fnew


    def drawpersonalbestpath(self, oldpos, newpos, idx):
        """ draw a path from old pos to new pos for the position idx """
        if self.isdraw:
            self.problem.visualiser.drawpath(oldpos, newpos, color = (0, 0, 0))  # draw the path;
            wx.Yield()



#___________________________________________________________________
# ref: wikipedia.com/Particle_swarm_optimization (for pso)
# PSO with Hill Climbing
class ParticleSwarmOptimizationHC(ParticleSwarmOptimization):
    def __init__(self, **kwargs):
        ParticleSwarmOptimization.__init__(self)  # inherit
        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user

        self.minimize = False

    def search(self):

        v = np.array([randin(-self.maxstep, self.maxstep) for _ in xrange(self.n)])  # initial velocities of the particles
        p = self.x.copy()  # best known position of each particle. make a hard copy of x
        fp = self.fx.copy()

        self.hcmaxstep = self.maxstep / 2

        # ## main loop
        while True:

            for i in xrange(self.n):  # #for each particle
                yield  # give control to caller. It will log and decide whether to stop.

                # ## old values
                xo = self.x[i].copy()
                vo = v[i].copy()
                po = p[i].copy()

                rp = np.random.uniform(0, 1, xo.shape)  # # produce a new position
                rg = np.random.uniform(0, 1, xo.shape)
                # new velocity
                # TODO: restart randomly when po-xo is very close to xbest-xo. Or xnew is too close to xbest
                vtmp = vo * self.w + (po - xo) * rp * self.psip + (self.xbest - xo) * rg * self.psig
                xtmp = xo + vtmp  #produce a new temporary position

                xnew, fnew = self.f(xtmp);yield  # correct position, compute its f, and update self.fbest and self.xbest
                self.updatex(xnew, fnew, i)  #update self.x[i],self.fx[i], and animate
                xnew, fnew = self.hillclimb(i, self.d);yield  # do a Hill Climb at this new position.


                v[i] = xnew - xo  # correct velocity

                if fnew > fp[i]:  # # update personal best
                    self.drawpersonalbestpath(p[i], xnew, i)
                    p[i] = xnew.copy()
                    fp[i] = fnew


#___________________________________________________________________
# ref: wikipedia.com/Particle_swarm_optimization
class ParticleSwarmOptimizationCustomDrawing(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit

        self.w = 0.90  # intertia weight
        self.psip = 0.10  #cognitive parameter
        self.psig = 0.60  #social parameter
        self.conf = 1.0  #constriction factor
        self.maxstepdivisor = 70
        self.name = 'PSO'
        self.npositions = 20
        self.customdraw = True

        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user

        self.minimize = False

    def search(self):

        ## if we want to do our own custom drawing:
        if self.customdraw == True:

            # shut down default automatic drawing. So that we can do our own
            self.isdraw = False

            # we will use self.problem.visualiser methods directly. let us
            # give it an easier name.
            vis = self.problem.visualiser

            ## let the visualiser draw the surface:
            # framework requiers vis to have a title
            vis.title = 'PSO - ' + self.problem.name

            # init() draws the surface. It accepts mlab.figure() keyword
            # arguments as
            # mlab_figure_opt dictionary. In the same way, it accepts
            # mlab.surf(), mlab.axes(), mlab.view(), mlab.title(),
            # mlab.outline() keyword arguments.
            vis.init(mlab_figure_opt = {'bgcolor':(.5, .5, .5)},
                     mlab_title_opt = {'size':0.4}
                     )

            ## reset the assessment count. It was incremented while drawing
            ## the surface.
            self.problem._assessmentcnt = 0




        v = np.array([randin(-self.maxstep, self.maxstep) for _ in xrange(self.n)])  # initial velocities of the particles
        p = self.x.copy()  # best known position of each particle. make a hard copy of x
        fp = self.fx.copy()

        ## draw initial positions of the particles. drawposition() can take
        ## any keyword argument mlab.points3d() accepts. See its documentation
        ## on
        ## mayavi web site.
        for e in self.x:
            vis.drawposition(e, color = (1, 0, .5))



        # ## main loop
        while True:
            for i in xrange(self.n):  # #for each particle
                yield  # give control to caller. It will log and decide whether to stop.

                # ## old values
                xo = self.x[i].copy()
                vo = v[i].copy()
                po = p[i].copy()

                rp = np.random.uniform(0, 1)  # # produce a new position
                rg = np.random.uniform(0, 1)
                # new velocity
                # TODO: restart randomly when po-xo is very close to xbest-xo. Or xnew is too close to xbest
                vtmp = self.conf * (vo * self.w + (po - xo) * rp * self.psip + (self.xbest - xo) * rg * self.psig)
                #xtmp = xo + vtmp
                xtmp = self.problem.stepby(xo, vtmp)

                xnew, fnew = self.f(xtmp); yield  # correct position, compute its f, and update self.fbest and self.xbest

                # just before updating the position, draw your path.
                # drawpath accepts any argument mlab.plot3d accepts. See its
                # documentation in mayavi web page.
                vis.drawpath(self.x[i], xnew, color = (0.1, 1, 1))

                self.updatex(xnew, fnew, i)

                v[i] = xnew - xo  # correct velocity

                if fnew > fp[i]:  # # update personal best
                    p[i] = xnew.copy()
                    fp[i] = fnew


