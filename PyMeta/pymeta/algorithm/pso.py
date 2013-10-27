import numpy as np

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
        self.minimize = False

        self.__dict__.update( **kwargs )  # overwrite defaults with keyword arguments supplied by user

    def search( self ):

        v = np.array( [randin( -self.maxstep, self.maxstep ) for _ in xrange( self.n )] )  # initial velocities of the particles
        p = self.x.copy()  # best known position of each particle. make a hard copy of x
        fp = self.fx.copy()

        # ## main loop
        while True:
            yield  # give control to caller. It will log and decide whether to stop.

            for i in xrange( self.n ):  # #for each particle

                # ## old values
                xo = self.x[i].copy()
                vo = v[i].copy()
                po = p[i].copy()

                rp = np.random.uniform( 0, 1, xo.shape )  # # produce a new position
                rg = np.random.uniform( 0, 1, xo.shape )
                vtmp = vo * self.w + ( po - xo ) * rp * self.psip + ( self.xbest - xo ) * rg * self.psig  # new velocity

                xtmp = xo + vtmp
                fnew, xnew = self.f( xtmp )

                self.updatex( xnew, fnew, i )
                v[i] = xnew - xo  # correct velocity

                if fnew > fp[i]:  # # update personal best
                    p[i] = xnew.copy()
                    fp[i] = fnew
                    if fnew > self.fbest:  # #update global best
                        self.updatebest( xnew, fnew )
                        yield  # give control to caller. It will log and decide whether to stop.

