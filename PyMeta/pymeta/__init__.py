"""

REFERENCES

[Luke13]: Essentials of Metaheuristics, Second Edition, Online Version 2.0,
    June, 2013
"""
from __future__ import division
import re
import matplotlib
#matplotlib.use("wx")
#matplotlib.use("TkAgg")
#matplotlib.use("QTAgg")
#matplotlib.use("QT4Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

import wx

from random import randint
import numbers
from mayavi import mlab
import time
from scipy import interpolate
from tvtk.tools import visual
import logging
import traceback
#import mlabwrap
import os, sys, random, numpy as np, inspect, pickle, uuid, collections, json
from pprint import pprint as pp
from textwrap import wrap
from inspect import getmembers, isroutine
import matplotlib.cm as cm



def mkdirfor(path):
    dn = os.path.dirname(path)
    if not os.path.isdir(dn):
        os.makedirs(dn)



def dprint(msg):
#    frame = inspect.currentframe()
#    stack_trace = traceback.format_stack(frame)
#    pp(stack_trace)
    print(str(msg))


def getlogger(filepath = '../tmp/log.txt', appname = 'PM'):
    #    # You can now start issuing logging statements in your code
#    lgr.debug('debug message')  # This won't print to myapp.log
#    lgr.info('info message')  # Neither will this.
#    lgr.warn('Checkout this warning.')  # This will show up in the log file.
#    lgr.error('An error goes here.')  # and so will this.
#    lgr.critical('Something critical happened.')  # and this one too.
    # create logger
    lgr = logging.getLogger(appname)
    lgr.setLevel(logging.DEBUG)
    # add a file handler
    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.WARNING)
    # create a formatter and set the formatter for the handler.
    frmt = logging.Formatter(
        '%(module)s:%(funcName)s:%(lineno)s - %(message)s')
    fh.setFormatter(frmt)
    # add the Handler to the logger
    lgr.addHandler(fh)
    return lgr

def rotationmatrixsuganthan(D, c, rotmatspath):
    dprint('initing mlabwrap')
    matlab = mlabwrap.init()
    dprint('inited mlabwrap')
    matlab.path(matlab.path(), rotmatspath)


    if not isinstance(D, list):
        D = [D]
    if not isinstance(c, list):
        c = [c]
    print D
    print c
    M = matlab.rot_mats(D, c)

    print M
    print 2
    return M


def rotationmatrix(D, c):
    """ Translated from the Matlab function rot_matrix of P. N. Suganthan"""

    A = np.random.normal(0, 1, (D, D))
    P, _ = np.linalg.qr(A)
    A = np.random.normal(0, 1, (D, D))
    Q, _ = np.linalg.qr(A)
    u = np.random.uniform(0, 1, (1, D))
    u = (u - u.min()) / (u.max() - u.min())
    D = (c ** u).ravel()
    D = np.diag(D)
    M = P.dot(D).dot(Q)
    return M


def minval(a, b):
    if a > b:
        return b
    else:
        return a

def maxval(a, b):
    if a > b:
        return a
    else:
        return b

def nparray(*args, **kwargs):
    """ Unless dtype is specified, makesure new array has float type """
    if 'dtype' not in kwargs:
        return np.array(*args, dtype = float, **kwargs)
    return np.array(*args, **kwargs)


def randin(lb, ub):
    """return random array with elements between the
    elements of lb and ub. ub is not included."""

    r = ((ub - lb) * np.random.random(np.shape(lb))
        + lb)


    return r

def randintbetween(mat1, mat2):
    """ return a matrix with random elements between
    elements of corresponding  mat1 and mat2 elements.
    """
    b = np.empty_like(mat1)
    nrows, ncols = mat1.shape
    for r in xrange(nrows):
        for c in xrange(ncols):
            b[r, c] = np.random.random_integers(
                mat1[r, c], mat2[r, c])
    return b

def randdiv(amount, cnt):
    """Divides the AMOUNT into CNT random parts and returns those
    parts in a numpy array. CNT must not be bigger than AMOUNT.
    Both CNT and AMOUNT must be integers.

    >>> random.seed(0)
    >>> randdiv(100,10)
    array([ 5,  6,  9,  8, 11, 15,  8,  9, 17, 12])

    """

    def argcheck(amount, cnt):
        if cnt > amount:
            raise Exception('cnt should be bigger or equal to amount')
        if not isinstance(amount, numbers.Integral):
            raise Exception('amount must be int')
        if not isinstance(cnt, numbers.Integral):
            raise Exception('cnt must be int')

    argcheck(amount, cnt)

    div = np.ones((cnt), dtype = int)
    rem = amount - cnt

    while rem > 0:
        div[random.randrange(0, cnt)] += 1
        rem -= 1
    return div

def overwrite(orig, **options):
    """
    overwrite already-existing/default values in the original
    dictionary with the ones in the options dictionary.
    if the options dictionary has keys that are not in orig, they
    are not assigned to orig. This function is intended for
    easy, safe option assignments in places like __init__()
    functions
    """

    for key in orig:
        if key in options:
            orig[key] = options[key]



class SetupClass(type):
    """ answer from :
        http://stackoverflow.com/questions/22261763
    """
    def __call__(cls, *args, **kwargs):
        # create the instance as normal.  this will invokoe the class's
        # __init__'s as expected.
        self = super(SetupClass, cls).__call__(*args, **kwargs)

        ## for each class in the class hierarchy (Default.setup() is first)
        for base in reversed(cls.__mro__):
            setup = vars(base).get('setup')
            # in the general case, we have to use the descriptor protocol
            # to setup methods/staticmethods/classmethods properly
            if hasattr(setup, '__get__'):
                setup = setup.__get__(self, cls)
            if callable(setup):
                setup()

        return self


class Default(object):
    __metaclass__ = SetupClass
    def __init__(self):
        pass

    def overwrite(self, **options):
        """
        overwrite already-existing/default values in self.dict '
        'with the ones in the options dictionary.
        if the options dictionary has keys that are not in orig, they
        are not assigned to orig. This function is intended for
        easy, safe option assignments in places like __init__()
        functions
        """

        overwrite(self.__dict__, **options)

#    def setup(self, **kwargs):
#        dprint('Default.setup')
#        pass


#     def __init__(self, **kwargs):
#         self.__dict__.update(**kwargs)

#     def __getattr__(self, attr):
#         return self.__dict__.get(attr, None)

#     def __repr__(self):
#         keys = [key for key in dir(self) if not key.startswith('_')]
#         return 'dict:'+str(self.__dict__)+'keys:'+str(keys)





# class Struct(Default):
#     """Class that can be used similar to a matlab struct"""
#     pass





class Table:
    def __init__(self):

        self.default_alignment = 'C'
        self.width = '\\linewidth'
        self.header_escape = {'#': '\#'}

        #TODO: make self.order readonly (by using property decorator?)
        self.order = collections.OrderedDict()
        self.table = []

    def row(self):
        self.table.append({})

    def add(self, col, content, **kwargs):
        self.order[col] = 1
        self.table[-1][col] = dict(name = col, content = content, **kwargs)

    def latex_data(self, fid):
        '''fid: file or similar. E.g. file or StringIO or ... any object
        that defines a proper write() method.'''
        for irow in range(len(self.table)):
            lst = []
            for colname in self.order:
                content = self.table[irow][colname]['content']
                content = str(content)
                lst.append(content)
            fid.write(' & '.join(lst) + '\\\\\n')

    def latex_header(self, fid):
        fid.write(' & '.join((self.hesc(key) for key in self.order.keys())) +
                  '\\\\\n')

    def latex_alignments_tabulary(self, fid):
        lst = []
        for colname in self.order:
            if 'align' in self.table[0][colname]:
                lst.append(self.table[0][colname]['align'])
            else:
                lst.append(self.default_alignment)
        fid.write('{' + ''.join(lst) + '}')

    def latex_tabulary(self, fid):
        fid.write('\\begin{tabulary}{%s}' % self.width)
        self.latex_alignments_tabulary(fid)
        fid.write('\\hline\n')
        self.latex_header(fid)
        fid.write('\\hline\n')
        self.latex_data(fid)
        fid.write('\\hline\n')
        fid.write('\\end{tabulary}\n')


    def dlt(self, astr):
        astr = astr.replace('[', '')
        astr = astr.replace(']', '')

    def hesc(self, astr):
        """escape special characters like #"""
        for key in self.header_escape:
            astr = astr.replace(key, self.header_escape[key])
        return astr


class FixBounds():
    """
    Namespace for static methods of fixing bounds
    """
    @staticmethod
    def to_edges(ob, pos):
        """ out of bounds dimensions are moved
        to edges."""
        high = pos > ob.ub
        low = pos < ob.lb
        pos[high] = ob.ub[high]
        pos[low] = ob.lb[low]
        return pos

    @staticmethod
    def full_random(ob, pos):
        high = pos > ob.ub
        low = pos < ob.lb
        if np.any(high) or np.any(low):
            pos = randin(ob.lb, ob.ub)
        return pos

    @staticmethod
    def exceeder_random(ob, pos):
        """ assign random values only to the
        dimensions that are out of bounds """
        high = pos > ob.ub
        low = pos < ob.lb
        hl = high | low
        if np.any(hl):
            pos[hl] = randin(ob.lb[hl], ob.ub[hl])

        return pos



from pymeta.utils.pymetautils import Default

class OptimizationVisualiser(Default):
    def __init__(self):
        Default.__init__(self)
        #self.title='Optimization Visualization'

    def setup(self):
        if self.problem is not None:
            if self.problem.minimize:
                self.fun = self.problem.cost
            else:
                self.fun = self.problem.quality

            self.lb = self.problem.lb
            self.ub = self.problem.ub
            self.step = (self.ub - self.lb) / float(self.stepdivisor)


def getcurveadder():
    npts = 100  # number of points to sample

    # describe your shape in 1d like this
    shape1 = np.array([0, .5, .75, .75, .5, 0])

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
    shape3 = np.vstack(
        [np.linspace(p1[dim], p2[dim], npts) for dim in xrange(3)]).T
    # raise the z coordinate
    shape3[:, -1] = shape3[:, -1] + adder[:, -1] * amp
    return shape3



class TwoDFunVisualiser3D(OptimizationVisualiser):
    def __init__(self, **kwargs):
        OptimizationVisualiser.__init__(self)  # inherit
        self.fun = None  # # defaults
        self.lb = None
        self.ub = None
        self.step = None
        self.isanimate = False
        self.problem = None
        self.__dict__.update(**kwargs)  # overwrite

        wx.Yield()


    def init(self, **kwargs):
        args = {}
        args['mlab_figure_opt'] = {}
        args['mlab_surf_opt'] = {}
        args['mlab_axes_opt'] = {}
        args['mlab_view_opt'] = {}
        args['mlab_title_opt'] = {}
        args['mlab_outline_opt'] = {}
        args.update(kwargs)

        # # prepare the surface data:
#         self.x = np.arange(self.lb[0], self.ub[0], self.step[0])
#         self.y = np.arange(self.lb[1], self.ub[1], self.step[1])

        lb = self.lb; ub = self.ub; step = self.step  # # shorter names

        x, y = np.mgrid[lb[0]:ub[0]:step[0], lb[1]:ub[1]:step[1]]
        def valf(a, b):
            return self.fun(np.array(list((a, b))).ravel())
        shape = x.shape
        x = x.reshape((-1, 1))
        y = y.reshape((-1, 1))
        z = np.empty_like(x)
        for i in xrange(x.size):
            z[i] = valf(x[i], y[i])

        mins = np.array([np.min(a) for a in (x, y, z)])
        maxs = np.array([np.max(a) for a in (x, y, z)])
        self.ranges = np.array([(mins[a], maxs[a]) for a in xrange(3)]).ravel()

        lens = np.array([100., 100., 30.])
        self.scaler = lens / (maxs - mins)

        xsc = x * self.scaler[0]
        ysc = y * self.scaler[1]
        zsc = z * self.scaler[2]

        z = zsc.reshape(shape)
        x = xsc.reshape(shape)
        y = ysc.reshape(shape)

        ## draw the surface
        opt = dict(size = (400, 400), bgcolor = (1, 1, 1), fgcolor = (0, 0, 0))
        opt.update(args['mlab_figure_opt'])
        self.fig = mlab.figure(**opt)

        visual.set_viewer(self.fig)

        opt = dict(colormap = 'gray', opacity = .5)
        opt.update(args['mlab_surf_opt'])
        self.surf = mlab.surf(x, y, z, **opt)

        # # add info
        opt = dict(ranges = self.ranges)
        opt.update(args['mlab_axes_opt'])
        mlab.axes(**opt)

        opt = dict(azimuth = 0, elevation = 60, distance = 'auto')
        opt.update(args['mlab_view_opt'])
        mlab.view(**opt)

        opt = {}
        opt.update(args['mlab_outline_opt'])
        mlab.outline(**opt)

        opt = dict(line_width = .5, opacity = .9, size = 2, height = 5)
        opt.update(args['mlab_title_opt'])
        mlab.title(self.title, **opt)
        # mlab.show_graphs()
        wx.Yield()

#    def drawbest(self, p):
#        pass

    def drawposition(self, p, **kwargs):
        pz = np.hstack((p, self.fun(p))) * self.scaler
        mlab.points3d(pz[0], pz[1], pz[2], **kwargs)
        wx.Yield()

    def drawbest(self, p, *args, **kwargs):
        self.drawposition(p, color = (1, 1, 0), scale_factor = 3)
        wx.Yield()

    def drawpath(self, p1, p2, **kwargs):
        if np.all(np.equal(p1, p2)):
            return

        op = dict()
        op['tube_radius'] = .2
        op['reset_zoom'] = False
        op.update(**kwargs)

        pz2 = np.hstack((p1, self.fun(p1))) * self.scaler
        pz1 = np.hstack((p2, self.fun(p2))) * self.scaler
        xyz = connectbycurve(pz2, pz1)
        mlab.plot3d(xyz[:, 0], xyz[:, 1], xyz[:, 2], figure = self.fig, **op)
        wx.Yield()
        if self.isanimate:
            print('sleeping')
            time.sleep(0.010)
            wx.Yield()

    def drawpathbest(self, p1, p2, *args, **kwargs):
        op = dict()
        op['color'] = (1, 1, 0)
        op['tube_radius'] = .5
        op.update(**kwargs)

        self.drawpath(p1, p2, *args, **op)

    def flush(self):
        wx.Yield()



class TwoDFunVisualiserColors(OptimizationVisualiser):
    def __init__(self, **kwargs):
        OptimizationVisualiser.__init__(self)  # inherit
        self.fun = None  # # defaults
        self.lb = None
        self.ub = None
        self.stepdivisor = 100
        self.isanimate = False
        self.problem = None
        self.__dict__.update(**kwargs)  # overwrite


        self.fig = None
        self.ax = None
        self.im = None
        self.cb = None




    def init(self, **kwargs):
        #### shorter names
        lb = self.lb;
        ub = self.ub;
        step = self.step

        #### prepare the surface data
        x = np.arange(lb[0], ub[0], step[0])
        y = np.arange(lb[1], ub[1], step[1])
        X, Y = np.meshgrid(x, y)
        sols = np.vstack((X.ravel(), Y.ravel())).T
        Z = np.array([self.fun(np.array(i, order = 'C')) for i in sols])
        Z = Z.reshape(X.shape)

        #### show the surface
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax

        self.im = self.ax.imshow(
            Z,
            interpolation = 'bilinear',
            origin = 'lower',
            #cmap = cm.get_cmap('gist_yarg'),
            cmap = cm.get_cmap('Greys_r'),
            extent = (x[0], x[-1], y[0], y[-1]))
        self.cb = self.fig.colorbar(self.im, use_gridspec = True)

        plt.tight_layout()
        self.ax.set_xlim(x[0], x[-1])
        self.ax.set_ylim(y[0], y[-1])
        plt.ion()
        plt.show()
        self.fig.canvas.flush_events()

    def drawposition(self, pt, *args, **kwargs):
        h = self.ax.plot(pt[0], pt[1], 'o', *args, **kwargs)
        return h

    def drawbest(self, pt, *args, **kwargs):
        return self.ax.plot(pt[0], pt[1], 'x', *args, color = (1, 1, 0),
            markersize = 9, **kwargs)

    def drawpath(self, pt1, pt2, *args, **kwargs):
        if np.all(np.equal(pt1, pt2)):
            return
        x = (pt1[0], pt2[0])
        y = (pt1[1], pt2[1])
        h = self.ax.plot(x, y, *args, **kwargs)
        return h

    def drawpathbest(self, pt1, pt2, *args, **kwargs):
        op = dict()
        op['color'] = (1, 1, 0)
        op['linewidth'] = 2
        op.update(**kwargs)

        return self.drawpath(pt1, pt2, *args, **op)

    def drawrange(self, pt, halfrange):
        x1, y1 = pt - halfrange
        x2, y2 = pt + halfrange
        verts = [
               (x1, y1),
               (x1, y2),
               (x2, y2),
               (x2, y1),
               (x1, y1),
               ]
        codes = [
                 Path.MOVETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.CLOSEPOLY,
                 ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, lw = 1, facecolor = 'none')
        self.ax.add_patch(patch)
#        self.ax.set_xlim(x1, x2)
#        self.ax.set_ylim(y1, y2)
        return patch

    def flush(self):
        plt.draw()
        self.fig.canvas.flush_events()

TwoDFunVisualiser = TwoDFunVisualiser3D

class DummyVisualiser(OptimizationVisualiser):
    def __init__(self, **kwargs):
        self.problem = None
        pass

    def init(self):
        pass

    def drawbest(self, p):
        pass

    def drawposition(self, p, **kwargs):
        pass

    def drawpath(self, p1, p2, **kwargs):
        pass

    def show(self):
        pass
    def flush(self):
        pass


class OptimizationAlgorithm(Default):
    def __init__(self):
        Default.__init__(self)

        self.name = '?'
        self.problem = None
        self.positions = None
        self.npositions = 20
        self.poscolors = None

        self.stop = None  #
        self.isdebug = False
        self.log = []
        self.maxstepdivisor = 100;
        self.hcmaxstepdivisor = 200
        self.minimize = False
        self._obfun = []
        self._drawbest = True
        self.deprecated_isbetter = False
        self.warn_selfupdate = False
        self.visualiser = None
        self.isdrawupdatex = True

        # self.__dict__.update(**kwargs)
    def draw(self):
        self.problem.visualiser.fig.draw()
        self.problem.visualiser.fig.canvas.flush_events()

    def f(self, poslist):
        ## get f and fixed positions
        if poslist.ndim == 1:
            #### fix position
            xfix = self.problem.fixposition(self.problem.fixbounds(poslist))

            #### get its value
            ffix = self._obfun(xfix)

            #### update best if necessary
            if self.isbetterNOTequal(ffix, self.fbest):
                self.updatebest(xfix, ffix)

            ### return
            return (xfix, ffix)

        elif poslist.ndim == 2:
            # recursively call itself
            xfix = np.empty_like(poslist)
            ffix = np.empty(poslist.shape[0])
            for i in xrange(poslist.shape[0]):
                xfix[i], ffix[i] = self.f(poslist[i])
            return (xfix, ffix)



    def run(self):
        if self.isdraw:
            ## prepares colors for each position
            self.poscolors = self.prepareposcolors()

        ## for deciding which value is better,
        ## which to use?
        def isbetter_deprecated(new, old):

            print('Warning: self.isbetter() is ' +
                    'deprecated. Use ' +
                    'self.isbetterORequal() or ' +
                    'self.isbetterNOTequal().')
            val = True
            if self.minimize:
                val = (new <= old)
            else:
                val = (new >= old)
            return val
        self.isbetter = isbetter_deprecated

        if self.minimize:
            self.isbetterORequal = (
                lambda new, old: new <= old)
            self.isbetterNOTequal = (
                lambda new, old: new < old)
            self._obfun = self.problem.cost
            self.fbest = float('inf')
        else:
            self.isbetterORequal = (
                lambda new, old: new >= old)
            self.isbetterNOTequal = (
                lambda new, old: new > old)
            self._obfun = self.problem.quality
            self.fbest = float('-inf')

        self.visualiser = self.problem.visualiser

        self.problem.resetassessmentcnt()
#        self.problem.positions = self.problem.positions.astype(float)

        self.positions = self.positions.astype(float)

        self.log = [];
        self.logfes=[]
        self.logfbest=[]
        cnt = {
            'assessmentcnt':0,
            'error':float('inf')
            }

        self.startclock = time.clock()


        #### fix positions, also get their objective
        #### values. dont draw the movement of best
        #### in this stage
        self._drawbest = False
        self.x, self.fx = self.f(self.positions)
        self.positions = self.x
        self._drawbest = True

        ## possibly needed info

        # number of positions
        self.n = self.x.shape[0]

        # number of dimensions on each position
        self.d = self.x.shape[1]
        self.hclimit = 2 * self.d

        ## initialize some important holders
        bestidx = 0
        if self.minimize:
            bestidx = self.fx.argmin()
        else:
            bestidx = self.fx.argmax()

        # best position
        self.xbest = self.x[bestidx].copy();

        # best value: global best value
        self.fbest = self.fx[bestidx]

        self.maxstep = (
            (self.problem.ub - self.problem.lb) / self.maxstepdivisor)
        self.problem.maxstep = self.maxstep

        self.hcmaxstep = (
            (self.problem.ub - self.problem.lb) / self.hcmaxstepdivisor)



        ## main loop
        yielder = self.search()

        oldbest = self.fbest
        while self.iscontinue():

            # run the actual search function till next yield
            yielder.next()

            if oldbest != self.fbest:
                oldbest = self.fbest
                try:
                    self.currenterror = abs(self.fbest - self.problem.optimum)
                except:pass

        self.dolastlog()
        self.stopclock = time.clock()

        ### negate elements of logfbest if necessary
        if self.minimize != self.problem.minimize:
            for i,e in enumerate(self.logfbest):
                self.logfbest[i] = -e

        ## draw final positions.
        self.drawfinalpositions()
        self.drawbest(self.xbest)

        return self.log



    def dolog(self):
#         self.log.append({
#             'assessmentcnt':
#                 self.problem.assessmentcnt(),
#             'fbest':self.fbest})
        self.logfes.append(self.problem.assessmentcnt())
        self.logfbest.append(self.fbest)

    def dolastlog(self):
        self.dolog()
#         self.log.append({
#             'assessmentcnt':
#                 self.problem.assessmentcnt(),
#             'fbest':self.fbest})



    def iscontinue(self):
        """ decide whether we should continue searching. """
        return self.problem.assessmentcnt() < self.stop['assessmentcnt']


    def updatex(self, xnew, fnew, i):
        if np.array_equal(self.x[i], xnew):
            if self.warn_selfupdate:
                dprint('updatex: warning! you are updating the x to the exact '
                       'same value! There may be an error in your '
                       'algorithm logic. You think you are modifying the x, '
                       'but '
                       'it is not being modified.')
        if self.isdrawupdatex:
            self.drawpath(self.x[i], xnew, i)
            self.drawbest(self.xbest)
            self.problem.visualiser.flush()

        self.x[i] = xnew
        self.fx[i] = fnew

    def hillclimb(self, i, hclimit = -1):
        count = 0


        if hclimit <= 0:
            hclimit = self.hclimit

        while (hclimit >= count):
            xtmp = (self.x[i]
                + randin(-self.hcmaxstep,
                    self.hcmaxstep))
            xnew, fnew = self.f(xtmp)
            if self.isbetter(fnew, self.fx[i]):
                self.updatex(xnew, fnew, i)
                count = 0
            else:
                count += 1

        return self.x[i].copy(), self.fx[i]

    def updatebest(self, xnew, fnew):
        #### draw the movement of best, if conditions hold
        if (self._drawbest and
            (self.fbest != float('inf')) and
            (self.fbest != float('-inf'))):
            self.drawpathbest(self.xbest, xnew)

        #### do actual updating
        self.xbest = xnew.copy()
        self.fbest = fnew.copy()

        #### the best changed. we should log
        self.dolog()

    def updateposnbest(self, xnew, fnew, i):
        """ if xnew is better than x, update x.
        if xnew is better than xbest, update xbest.
        """
        print('deprecated. just use self.updatex')
        # update position of this ascender
        if self.isbetter(fnew , self.fx[i]):
            self.updatex(xnew, fnew, i)

            # update global best
            if self.isbetter(fnew, self.fbest):
                self.updatebest(xnew, fnew)

################# start drawing related methods

    def bestcolor(self):
        return (1, 1, 0)


    def prepareposcolors(self):
        poscolors = None
        if self.isdraw:
            poscolors = []
            for _ in self.positions:
                color = tuple(np.random.uniform(0, 1, (3,)).tolist())
                poscolors.append(color)
        return poscolors



    def drawbest(self, pos):
        if self.isdraw:
            self.problem.visualiser.drawbest(pos)

    def drawfinalpositions(self):
        if self.isdraw:
            for i in xrange(self.n):
                self.problem.visualiser.drawposition(
                    self.positions[i],
                    color = self.poscolors[i])

    def drawpath(self, oldpos, newpos, idx):
        """ draw a path from old pos to new pos for the position idx """
        if self.isdraw:
            self.problem.visualiser.drawpath(oldpos, newpos,
                color = self.poscolors[idx])

    def drawpathbest(self, oldpos, newpos):
        """ draw paths of the best."""
        if self.isdraw:
            self.problem.visualiser.drawpathbest(oldpos, newpos,
                                             color = self.bestcolor())
###end drawing related methods ###


class OptimizationProblem(Default):
    def __init__(self, **kwargs):
        dprint('OptimizationProblem.__init__')
        Default.__init__(self)  # inherit

        self.lb = np.array([0, 0, 0, 0], dtype = float)
        self.ub = np.array([.1, 2, 3, 40], dtype = float)
        self.name = None
        self.info = None
        self.visualiser = None
        self.visualiser_class = None

        # set true if this is a minimization problem
        self.minimize = False
        self.isdebug = False
        self.isdebugprintassessments = False

        # theoretical best value, or optimum,
        # for the problem
        self.optimum = None

        self.ndims = None

#        self.fixboundsfun = FixBounds.to_edges
        self.fixboundsfun = FixBounds.exceeder_random


        self.tweakmethod = 'justsum'
        self.tweaksubmethod = 'bucclosed'

        # probability of adding noise to an element in solution vector
        self.tweakprob = 0.10

        self.warnnotweak = False

        # method of stepping from x to x+v
        self.stepbymethod = 'adaptivenotsame'
        self.stepbydivisor = 100.0
        self.configisdone = False

        self.isshift = False
        self.isrotate = False
        self.rotmatrix_c = 2
        self.isrotatesuganthan = False
        self.rotmatspath = os.path.abspath('../../../../alien')

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.__dict__.update(**kwargs)  # overwrite

        self._assessmentcnt = 0

        # maxstep is set by the algorithm on runtime
        self.maxstep = (self.ub - self.lb) / 100
        self.shiftvector = None

    def setup(self, **kwargs):
        dprint('OptimizationProblem.setup')
        self.ub = self.ub.astype(float)
        self.lb = self.lb.astype(float)

        if self.ndims:
            print "setting dims"
            self.ub = np.ones(self.ndims) * self.ub[0]
            self.lb = np.ones(self.ndims) * self.lb[0]
            try:
                self.optimumsol = np.ones(self.ndims) * self.optimumsol[0]
            except:
                pass

        if self.isshift:
            print "setting shifting"
            self.shiftvector = self.getshiftvector()
        if self.isrotate:
            print "setting rotation"
            self.rotationmatrix = self.getrotationmatrix()
#            self.ub = self.shiftNrotate(self.ub)
#            self.lb = self.shiftNrotate(self.lb)

        if self.minimize:
            self.value = self.cost
        else:
            self.value = self.height

        try:
            self.visualiser = self.visualiser_class(problem = self)
        except Exception:
            pass


    def getdims(self):
        print "getdimscalled"
        return len(self.ub)
    dims = getdims

    def getshiftvector(self):
        #return np.array([4, 4])
        #return randin(self.lb, self.ub)

        #idea: when all x is shifted to x+adder, optimumsol is shifted to
        #optimumsol-adder. So: lb <= optimumsol-adder <=ub. From there one
        #can obtain optimumsol-ub <= adder <= optimumsol-lb
        adder = randin(self.optimumsol - self.ub, self.optimumsol - self.lb)
        dprint('shiftvector:' + str(adder))
        return adder

    def getrotationmatrix(self):
        D = self.ub.size
        c = self.rotmatrix_c
        if self.isrotatesuganthan:
            M = rotationmatrixsuganthan(D, c, self.rotmatspath)
        else:
            M = rotationmatrix(D, c)

        return M
    def assessmentcnt(self):
        return self._assessmentcnt

    def resetassessmentcnt(self):
        self._assessmentcnt = 0

    def quality(self, position):
        return self.height(position)

    def height(self, position):
        if self.isshift or self.isrotate:
            position = self.shiftNrotate(position)

        h = self.heightfun(position)
        self._assessmentcnt = self._assessmentcnt + 1;
        if self.isdebugprintassessments:
            if self.minimize:
                print self.assessmentcnt(), -h
            else:
                print self.assessmentcnt(), h
        return h

    def cost(self, position):
        h = self.height(position)
        return -1 * h

    def heightfun(self, x):
        return -self.costfun(x)

    def costfun(self, x):
        return -self.heightfun(x)

    def randpos(self):
        return randin(self.lb, self.ub)

    def randposn(self, nrows):
        # print 'randposn:', self.lb, nrows
        ncols = self.lb.size
        mat = np.empty((nrows, ncols))
        for i in xrange(nrows):
            mat[i] = self.randpos();
        return mat

    def pos2str(self, pos):
        return str(pos)

    def fixposition(self, pos):
        """fix problems about position:
        invalid, etc."""
        return pos

    def fixbounds(self, pos):
        return self.fixboundsfun(self, pos)

    def tweak(self, pos):

        t = self.tweakfun(pos)
        f = self.fixposition(t)
        if self.warnnotweak and np.array_equal(pos, f):
            print ('Warning: ' + str(self.tweakfun) + ' is supposed to change the '
                            'solution. But apparantly it can not :). '
                            'solution: ' + str(pos) + 'tweak:' + str(f))
        return f

    def tweakfun(self, apos, method = None, submethod = None):
        # TODO: instead of if method == ... use different methods. it is easier
        # to debug.

        ## handle args
        if not(method):
            method = self.tweakmethod

        if not(submethod):
            submethod = self.tweaksubmethod

        ## based on the method, do your thing.
        if method == 'fast':
            ##fast but careless tweaking .
            ##    1) all elements are tweaked.
            ##    2) lb and ub are not checked.

            pos = apos + randin(-self.maxstep, self.maxstep)

        elif method == 'bucclosed':
            ##Bounded Uniform Convolution Single Trial.
            ##
            ##    Like tweak_buc but we also make sure
            ##        we get a nice value in the first trial.
            ##
            ##renaming:
            ##    ob.tweakprob <- p
            ##    pos <- v
            ##    ob.maxstep <- r
            ##    ob.lb <- min
            ##    ob.ub <- max

            pos = apos.copy()

            ## make sure at least one element is changed
            favored = random.randrange(len(pos))

            for i, e in enumerate(pos):
                ## for each element in the array

                if (self.tweakprob >= random.uniform(0, 1)) or (i == favored):
                    ## lucky element. will tweak.

                    ## get an in-range random value
                    pos[i] = random.uniform(
                        maxval(self.lb[i], e - self.maxstep[i]),
                        minval(self.ub[i], e + self.maxstep[i]))

        elif method == 'adaptmaxstep':
            if submethod == 'adaptmaxstep':
                raise Exception('submethod can not be same as method')

            while True:
                tmp = self.tweakfun(apos, submethod)
                pos = self.fixposition(tmp)
                if not(np.array_equal(apos, pos)):
                    break
                self.maxstep *= 2

        elif method == 'int_single_random':
            pos = apos.copy()

            while True:
                dim = random.randrange(self.ub.size)
                pos[dim] = random.randint(self.lb[dim], self.ub[dim])
                if not(np.array_equal(pos, apos)):
                    break
        elif method == 'tweak1dim':
            ''' tweaks only one random dimension '''
            pos = apos.copy()
            dim = random.randrange(self.ub.size)
            pos[dim] = np.random.uniform(self.lb[dim], self.ub[dim])

        return pos

    def stepby(self, pos, step):
        t = self.stepbyfun(pos, step)
        f = self.fixposition(t)
        if np.array_equal(pos, f):
            print(' warning: ' + str(self.tweakfun) + ' could not change the '
                            'solution. baaad. solution was ' + str(pos) +
                            ' and step was ' + str(step))
        return f

    def stepbyfun(self, pos, step):

        if   self.stepbymethod == 'adaptivenotsame':
            while True:
                t = pos + step
                newpos = self.fixposition(t)
                if not(np.array_equal(pos, newpos)): break
                #too small step?
                step = step * 2
                srange = self.ub - self.lb
                #too large step?
                if any(step > srange):
                    step = step / self.stepbydivisor

        elif self.stepbymethod == 'justsum':
            newpos = pos + step
        else:
            raise Exception('we do not know such stepbymethod ...')

        return newpos


    def shiftNrotate(self, pos):
        if self.isshift:
            pos = self.shiftvector + pos

        if self.isrotate:
            pos = pos.dot(self.rotationmatrix)

        return pos


class RandomSearch(OptimizationAlgorithm):
    """
    Simplest blind random search metaheuristics.
    Just check random positions till termination.
    """

    def __init__(self, **kwargs):
        # inherit
        OptimizationAlgorithm.__init__(self)

        self.name = 'rs'

        # overwrite defaults with keyword arguments
        # supplied by user
        self.__dict__.update(**kwargs)
        self.npositions = 1
        #assume this is a minimization algorithm.
        self.minimize = True

    def search(self):
        while True:
            yield
            self.f(self.problem.randpos())





class GenericExperiment(Default):
    def __init__(self, **kwargs):
        Default.__init__(self)
        self.isdraw = True
        self.isdrawupdatex = True
        self.isanimate = True
        self.isplotconvergence = True
        self.convergenceplottype = 'semilogy'
        self.isdebug = False
        self.stop = {'assessmentcnt':20}
        self.ntrials = 2
        self.problemlist = None
        self.algorithmlist = None
        self.returntrials = False
        self.writetrials = True
        self.writedir = '../tmp/results'
        self.logdir = 'c:/temp/pymeta/'
        self.imdir = '../latex/graphics'
        self.sep = '____',
        self.dashes = [],
        self.exptime = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        self.tmpdir = os.getcwd() + '/../latex/tmp/'
        self.expdir = self.tmpdir + self.exptime
        self.ndims = None
        self.logfile = None
        self.logfilepath = None
        self.__dict__.update(**kwargs)


    def do(self):
        results = []

        #### re-check options
        if self.ntrials > 1:
            print('Warning: ntrials is higher than 1. So turning 3d drawing ' +
                  'and animation off.')
            self.isdraw = False
            self.isanimate = False

        self.expdir = os.path.normpath(self.expdir)

        #### run multitrials for each problem-algorithm triple

        for probleminfo in self.problemlist:
            for algorithminfo in self.algorithmlist:
                for trial in range(self.ntrials):

                    problem = probleminfo['class'](ndims = self.ndims,
                            **probleminfo)

                    algorithm = algorithminfo['class'](**algorithminfo)
                    algorithm.isdrawupdatex = self.isdrawupdatex

                    log = self.runonce(algorithm, problem, trial)


                    trialinfo = dict(algorithm = algorithm, problem = problem,
                        trial = trial, log = log)

                    if self.returntrials:
                        results.append(trialinfo)
                    if self.writetrials:
                        self.writelog(trialinfo)

        return results


    def runonce(self, algorithm, problem, trial):

        graphtitle = (problem.name + ' - ' + algorithm.name +
                      ' - trial' + str(trial))
        if self.isdebug:
            print graphtitle

        if self.isdraw:
#            problem.visualiser = problem.visualiserclass(
#                fun = problem.cost, lb = problem.lb, ub = problem.ub,
#                step = (problem.ub - problem.lb) / 100)
            problem.visualiser.title = graphtitle
            problem.visualiser.init()
            problem.visualiser.isanimate = self.isanimate

        problem.isdebug = self.isdebug
        problem.isdebugprintassessments = self.isdebugprintassessments

        algorithm.isdraw = self.isdraw
        algorithm.problem = problem
        algorithm.positions = problem.randposn(algorithm.npositions)
        algorithm.stop = self.stop
        algorithm.isdebug = self.isdebug
        log = algorithm.run()
        return log



    def writelog(self, t):
        algo = t['algorithm']
        prob = t['problem']

        for dumptype in [
                         'json',
                         #'pickle',
                         ]:
            filename = '__'.join((
                                 self.logdir,
                                 prob.name,
                                 algo.name,
                                 str(t['trial']),
                                 #str(uuid.uuid4()),
                                 dumptype,
                                 '.pymeta.trial.log.txt'))
            print('log: {}'.format(filename))

            if dumptype == 'json':
                with open(filename, 'wb') as fd:
                    logdict=dict()
                    logdict['algorithm_name']=algo.name
                    logdict['problem_name']=prob.name
                    logdict['trial']=t['trial']
                    #logdict['log']=t['log']
                    logdict['elapsed_time']=algo.stopclock-algo.startclock
                    logdict['algorithm_minimize']=algo.minimize
                    logdict['problem_minimize']=prob.minimize

                    try:logdict['problem_optimum']=prob.optimum
                    except:pass

                    logdict['logfes']=algo.logfes
                    logdict['logfbest']=algo.logfbest

                    try:logdict['algorithm_stop_error']=algo.stop['error']
                    except: pass

                    try:logdict['algorithm_stop_assessmentcnt']=algo.stop['assessmentcnt']
                    except: pass


                    json.dump(logdict, fd)
            if dumptype == 'pickle':
                with open(filename,'wb') as fd:
                    pickle.dump(t,fd)


import algorithm
import problem
import visualiser

def main():

    class Shouter:
        def __init__(self, name, shoutfun):
            self.name = name
            self.shout = shoutfun

        def shoutfun1(self):
            print('I am ' + self.name)

        def shoutfun2(self):
            print('This is ' + self.name)

    s1 = Shouter('ozi', Shouter.shoutfun1)
    s1.shout(s1)

    s2 = Shouter('ali', Shouter.shoutfun2)
    s2.shout(s1)

if __name__ == '__main__':
    main()
