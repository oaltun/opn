from pymeta.utils.pymetautils import randin, Default
import numpy as np
class GenericOptimizationProblem(Default):
    def __init__(self,**kwargs):
        Default.__init__(self) #inherit
        self.heightfun = None; ##defaults
        self.lb = None
        self.ub = None
        self.name = None
        self.visualiser = None
        self.__dict__.update(**kwargs) #overwrite

    def height(self,position):
        return self.heightfun(self.fixposition(position))
    
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