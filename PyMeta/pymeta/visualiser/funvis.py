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
from mayavi import mlab
import time
from scipy import interpolate
from tvtk.tools import visual
import wx

# mpl.rcParams['legend.fontsize']=10



from pymeta.visualiser.visualiserbase import OptimizationVisualiser


def getcurveadder():
    npts = 100  # number of points to sample
    shape1 = np.array([0, .5, .75, .75, .5, 0])  # describe your shape in 1d like this

    # get the adder. This will be used to raise the z coords
    x = np.arange(shape1.size)
    xnew = np.linspace(x[0], x[-1] , npts)  # sample the x coord
    tck = interpolate.splrep(x, shape1, s = 0)
    adder = interpolate.splev(xnew, tck, der = 0)
    adder[0] = adder[-1] = 0
    adder = adder.reshape((-1, 1))
    return adder

def connectbycurve(p1, p2, adder = getcurveadder()):
    dist = np.sum((p2 - p1) ** 2) ** 0.5
    # amp = dist/2.0
    amp = dist / 2
    npts = adder.size
    # get a line between points
    shape3 = np.vstack([np.linspace(p1[dim], p2[dim], npts) for dim in xrange(3)]).T
    # raise the z coordinate
    shape3[:, -1] = shape3[:, -1] + adder[:, -1] * amp
    return shape3



class TwoDFunVisualiser(OptimizationVisualiser):
    def __init__(self, **kwargs):
        OptimizationVisualiser.__init__(self)  # inherit
        self.fun = None  # # defaults
        self.lb = None
        self.ub = None
        self.step = None
        self.isanimate = False
        self.__dict__.update(**kwargs)  # overwrite

        wx.Yield()


    def init(self):
        # # prepare the surface data:
#         self.x = np.arange(self.lb[0], self.ub[0], self.step[0])
#         self.y = np.arange(self.lb[1], self.ub[1], self.step[1])

        lb = self.lb; ub = self.ub; step = self.step  # # shorter names

        x, y = np.mgrid[lb[0]:ub[0]:step[0], lb[1]:ub[1]:step[1]]
        def f(a, b): return self.fun(np.array(list((a, b))))
        shape = x.shape
        x = x.reshape((-1, 1))
        y = y.reshape((-1, 1))
        z = np.array([f(x[i], y[i]) for i in xrange(x.size)])
        mins = np.array([np.min(a) for a in (x, y, z)])
        maxs = np.array([np.max(a) for a in (x, y, z)])
        self.ranges = np.array([(mins[a], maxs[a]) for a in xrange(3)]).ravel()

        lens = np.array([100., 100., 20.])
        self.scaler = lens / (maxs - mins)

        xsc = x * self.scaler[0]
        ysc = y * self.scaler[1]
        zsc = z * self.scaler[2]

        z = zsc.reshape(shape)
        x = xsc.reshape(shape)
        y = ysc.reshape(shape)

        # # draw the surface
        self.fig = mlab.figure(size = (400, 400), bgcolor = (1, 1, 1), fgcolor = (0, 0, 0))
        visual.set_viewer(self.fig)
        self.surf = mlab.surf(x, y, z, colormap = 'gray', opacity = .5)

        # # add info
        mlab.axes(ranges = self.ranges)
        # mlab.view(0, 0,.25)
        mlab.outline()
        # mlab.title(self.title,line_width=.5,opacity=.9, size=2,height=5)
        mlab.title(self.title)
        # mlab.show()
        wx.Yield()

    def drawbest(self, p):
        pass

    def drawposition(self, p, **kwargs):
        pz = np.hstack((p, self.fun(p))) * self.scaler
        mlab.points3d(pz[0], pz[1], pz[2], **kwargs)
        wx.Yield()

    def drawpath(self, p1, p2, **kwargs):
        if np.all(np.equal(p1, p2)):
            return
        pz1 = np.hstack((p1, self.fun(p1))) * self.scaler
        pz2 = np.hstack((p2, self.fun(p2))) * self.scaler
        # xyz=np.vstack((pz1,pz2))
        xyz = connectbycurve(pz1, pz2)
        mlab.plot3d(xyz[:, 0], xyz[:, 1], xyz[:, 2], figure = self.fig, **kwargs)
        wx.Yield()
        if self.isanimate:
            print('sleeping')
            time.sleep(0.010)
            wx.Yield()


    def show(self):
        mlab.show()
