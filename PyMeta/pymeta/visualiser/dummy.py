'''
Created on 10 May 2013

@author: oguz
'''

from pymeta.visualiser.visualiserbase import OptimizationVisualiser

class DummyVisualiser(OptimizationVisualiser):
    def __init__(self, **kwargs):
        pass
        
    def init(self):
        pass
            
    def drawbest(self,p):
        pass
    
    def drawposition(self,p,**kwargs):
        pass
        
    def drawpath(self,p1,p2,**kwargs):
        pass
            
    def show(self):
        pass
    