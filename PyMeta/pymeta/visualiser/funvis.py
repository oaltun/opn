'''
Created on 10 May 2013

@author: oguz
'''
import numpy as np

class TwoDFunCurveVisualiser:
    fun = None  # function to visualise
    lb = None
    ub = None
    step = None
    def __init__(self,**kwargs):
        self.__dict__.update(**kwargs) #overwrite
        
        x0=np.arange(self.lb[0],self.ub[0],self.step[0])
        x1=np.arange(self.lb[1],self.ub[1],self.step[1])
    
        