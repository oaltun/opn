'''
Created on 10 May 2013

@author: oguz
'''
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

#mpl.rcParams['legend.fontsize']=10



from pymeta.visualiser.visualiserbase import OptimizationVisualiser

class TwoDFunVisualiser(OptimizationVisualiser):
    def __init__(self, **kwargs):
        OptimizationVisualiser.__init__(self)  # inherit
        self.fun = None  # #set defaults
        self.lb = None
        self.ub = None
        self.step = None
        self.__dict__.update(**kwargs)  # overwrite
        
        x = np.arange(self.lb[0], self.ub[0], self.step[0])
        y = np.arange(self.lb[1], self.ub[1], self.step[1])
        
        xx , yy= np.meshgrid(x, y)
        xxx = xx.reshape((-1,1))
        yyy = yy.reshape((-1,1))
        xy=np.hstack((xxx,yyy))
        zz = np.array([self.fun(pos) for pos in xy]).reshape(xx.shape)
        self.x=xx
        self.y=yy
        self.z=zz
        self.maxval = np.max(zz)
        
    def init(self):
        self.fig = plt.figure()
        self.ax  = self.fig.gca(projection='3d')
        self.surf = self.ax.plot_surface(self.x,self.y,self.z, rstride=10,cmap=cm.coolwarm , cstride=10, linewidth=0, antialiased=False)
        plt.ion()
        plt.hold(True)

    def drawbest(self,p):
        pass
    def drawposition(self,p):
        pass
    def drawpath(self,p1,p2):
        z1=self.fun(p1)
        z2=self.fun(p2)
        x=[p1[0],p2[0]]
        y=[p1[1],p2[1]]
        z=[z1,z2]
        print 'x y z', x,y,z
        self.ax.plot(x,y,z)
        plt.ion()
        plt.show()
        if self.isanimate:
            plt.pause(0.01)
        