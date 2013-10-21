from pymeta.utils.pymetautils import randin, Default
import numpy as np
class GenericOptimizationProblem( Default ):
    def __init__( self, **kwargs ):
        Default.__init__( self )  # inherit
        # self.heightfun = None; ##defaults
        self.lb = None
        self.ub = None
        self.name = None
        self.visualiser = None
        self.minimize = False  # set true if this is a minimization problem

        self.__dict__.update( **kwargs )  # overwrite
        self._assessmentcnt = 0

    def assessmentcnt( self ):
        return self._assessmentcnt

    def height( self, position ):
        h = self.heightfun( self.fixposition( position ) )
        self._assessmentcnt = self._assessmentcnt + 1;
        if self.minimize:
            print self.assessmentcnt(), -h
        else:
            print self.assessmentcnt(), h
        return h

    def cost( self, position ):
        return -1 * ( self.height( position ) )

    def heightfun( self, x ):
        return -self.costfun( x )

#     def costfun( self, x ):
#         return -self.heightfun( x )

    def randpos( self ):
        return randin( self.lb, self.ub )

    def randposn( self, nrows ):
        # print 'randposn:', self.lb, nrows
        ncols = self.lb.size
        mat = np.empty( ( nrows, ncols ) )
        for i in xrange( nrows ):
            mat[i] = self.randpos();
        return mat

    def pos2str( self, pos ):
        return str( pos )

    def fixposition( self, pos ):
        """fix problems about position: invalid, etc."""
        return pos

    def fixbounds( self, pos ):
        """fix out of boundary situation"""
        high = pos > self.ub
        low = pos < self.lb
        pos[high] = self.ub[high]
        pos[low] = self.lb[low]
        return pos
