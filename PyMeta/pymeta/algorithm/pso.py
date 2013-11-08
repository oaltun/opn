import numpy as np
import wx

from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin

# ref: wikipedia.com/Particle_swarm_optimization
class ParticleSwarmOptimization( OptimizationAlgorithm ):
    def __init__( self, **kwargs ):
        OptimizationAlgorithm.__init__( self )  # inherit

        self.w = 0.90  # # defaults
        self.psip = 0.10
        self.psig = 0.60
        self.maxstepdivisor = 70
        self.name = 'PSO'
        self.npositions = 20

        self.__dict__.update( **kwargs )  # overwrite defaults with keyword arguments supplied by user

        self.minimize = False

    def search( self ):

        v = np.array( [randin( -self.maxstep, self.maxstep ) for _ in xrange( self.n )] )  # initial velocities of the particles
        p = self.x.copy()  # best known position of each particle. make a hard copy of x
        fp = self.fx.copy()

        # ## main loop
        while True:
            for i in xrange( self.n ):  # #for each particle
                yield  # give control to caller. It will log and decide whether to stop.

                # ## old values
                xo = self.x[i].copy()
                vo = v[i].copy()
                po = p[i].copy()

                rp = np.random.uniform( 0, 1, xo.shape )  # # produce a new position
                rg = np.random.uniform( 0, 1, xo.shape )
                # new velocity
                # TODO: restart randomly when po-xo is very close to xbest-xo. Or xnew is too close to xbest
                vtmp = vo * self.w + ( po - xo ) * rp * self.psip + ( self.xbest - xo ) * rg * self.psig
                xtmp = xo + vtmp
                xnew, fnew = self.f( xtmp )  # correct position and get its f

                self.updatex( xnew, fnew, i )
                v[i] = xnew - xo  # correct velocity

                if fnew > fp[i]:  # # update personal best
                    self.drawpersonalbestpath( p[i], xnew, i )
                    p[i] = xnew.copy()
                    fp[i] = fnew
                    if fnew > self.fbest:  # #update global best and yield
                        self.updatebest( xnew, fnew )

    def drawpersonalbestpath( self, oldpos, newpos, idx ):
        """ draw a path from old pos to new pos for the position idx """
        if self.isdraw:
            self.problem.visualiser.drawpath( oldpos, newpos, color = ( 0, 0, 0 ), tube_radius = .1, opacity = .8 )  # draw the path;
            wx.Yield()
