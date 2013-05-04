from pymetautils import randin

class GenericOptimizationProblem:
    def __init__(self):
        self.heightfun = lambda x: x[0]
        self.lb=[]
        self.ub=[]
        self.name='?'
        self.visualiser=[]
        
    def height(self,position):
        return self.heightfun(self.fixposition(position))
    
    def randomposition(self):
        return randin(self.lb,self.ub)