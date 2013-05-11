from pymeta.utils.pymetautils import randin, Default
import numpy as np
class GenericOptimizationProblem(Default):
    heightfun = lambda x: x[0]
    lb=np.array([]); #must be a numpy array
    ub=np.array([]); #must be a numpy array
    name='?'
    visualiser=[]  
        
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