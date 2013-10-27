
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin

# HillClimbing:
class HillAscend( OptimizationAlgorithm ):
    def __init__( self, **kwargs ):
        OptimizationAlgorithm.__init__( self )  # inherit

        self.name = 'ha'
        self.minimize = False  # if True, assume the problem is to be minimized by this algorithm.
        self.maxstepdivisor = 40
        self.__dict__.update( **kwargs )  # overwrite defaults with keyword arguments supplied by user

    def search( self ):

        # ## main loop
        while True:  # while we have time

            for i in xrange( self.n ):  # #for each climber i

                # ## peek: take a look to a close to this position: xnew
                xnew = self.x[i] + randin( -self.maxstep, self.maxstep )
                xfix = self.problem.fixposition( self.problem.fixbounds( xnew ) )
                fnew = self.f( xfix )

                # if xnew is better than x[i], update x[i]. if xnew is better than xbest, update xbest.
                self.updateposnbest( xfix, fnew, i )

                yield  self.xbest, self.fbest, self.iteration  # let the controller decide whether stop or continue.






