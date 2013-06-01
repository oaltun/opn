from pymeta.utils.pymetautils import randin, Default
import numpy as np
class GenericOptimizationProblem(Default):
    def __init__(self,**kwargs):
        Default.__init__(self) #inherit
        #self.heightfun = None; ##defaults
        self.lb = None
        self.ub = None
        self.name = None
        self.visualiser = None
        self.__dict__.update(**kwargs) #overwrite
        self._assessmentcnt=0

    def height(self,position):
        h=self.heightfun(self.fixposition(position))
        self._assessmentcnt = self._assessmentcnt+1; print self.assessmentcnt(),h
        return h
    
    def assessmentcnt(self):
        return self._assessmentcnt
    
    def cost(self,position):
        return -1*( self.height(position))
    
    def randpos(self):
        return randin(self.lb,self.ub)
    
    def randposn(self,nrows):
        ncols = self.lb.size
        mat = np.empty((nrows,ncols))
        for i in xrange(nrows):
            mat[i]=self.randpos();
        return mat
    
    def pos2str(self,pos):
        return str(pos)
        
    def fixposition(self,pos):
        return pos