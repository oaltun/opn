"""

REFERENCES

[Luke13]: Essentials of Metaheuristics, Second Edition, Online Version 2.0,
    June, 2013
"""
from __future__ import division

import matplotlib
#matplotlib.use("wx")
#matplotlib.use("TkAgg")
#matplotlib.use("QTAgg")
matplotlib.use("QT4Agg")
import matplotlib.pyplot as plt

import wx

from random import randint
import numbers
from mayavi import mlab
import time
from scipy import interpolate
from tvtk.tools import visual
import logging
import traceback
import mlabwrap
import os, sys, random, numpy as np, inspect, pickle, uuid, collections
from pprint import pprint as pp
from textwrap import wrap
from inspect import getmembers, isroutine



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



class TwoDFunVisualiser(OptimizationVisualiser):
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

    def drawpath(self, p1, p2, **kwargs):
        if np.all(np.equal(p1, p2)):
            return
        pz2 = np.hstack((p1, self.fun(p1))) * self.scaler
        pz1 = np.hstack((p2, self.fun(p2))) * self.scaler
        xyz = connectbycurve(pz1, pz2)
        mlab.plot3d(xyz[:, 0], xyz[:, 1], xyz[:, 2], figure = self.fig,
            **kwargs)
        wx.Yield()
        if self.isanimate:
            print('sleeping')
            time.sleep(0.010)
            wx.Yield()


    def show_graphs(self):
        print('huh? ' + __file__)
        #mlab.show_graphs()


class DummyVisualiser(OptimizationVisualiser):
    def __init__(self, **kwargs):
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


class OptimizationAlgorithm(Default):
    def __init__(self):
        Default.__init__(self)

        self.name = '?'
        self.problem = None
        self.positions = None
        self.npositions = 20

        # self.stop={'time':0, 'fbest': float('inf'),
        # 'yieldcnt':float('inf') }
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

        # self.__dict__.update(**kwargs)

    def f(self, poslist):
        ## get f and fixed positions
        if poslist.ndim == 1:
            #### fix position
            xfix = self.problem.fixposition(
                self.problem.fixbounds(poslist))

            #### get its value
            ffix = self._obfun(xfix)

            #### draw the position
            if self.isdraw:
                self.problem.visualiser.drawposition(
                    xfix, color = (.5, .5, .5),
                    scale_factor = 1)
                wx.Yield()


            #### update best if necessary
            if self.isbetterNOTequal(
                ffix, self.fbest):
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

        ## for deciding which value is better,
        ## which to use?
        def isbetter_deprecated(new, old):
            if self.deprecated_isbetter:
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

        self.problem.resetassessmentcnt()
#        self.problem.positions = self.problem.positions.astype(float)

        self.positions = self.positions.astype(float)

        self.log = [];
        cnt = {
#            'fbest': self.fbest,
#            'time':0,
#            'yieldcnt':0,
            'assessmentcnt':0,
            'nerror': float('-inf'),
            'error':float('inf')
            }


        ## fix positions, also get their objective
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

        ## prepares colors for each position
        self.prepareposcolors()

        ## main loop
        self.yieldcnt = 0;
        yielder = self.search()
        oldbest = self.fbest
        while self.iscontinue(cnt, self.stop):
            self.yieldcnt += 1

            # run the actual search function till
            # next yield
            yielder.next()
            cnt['assessmentcnt'] = self.problem.assessmentcnt()

            if oldbest != self.fbest:
                oldbest = self.fbest
                if (hasattr(self.problem, 'optimum')
                    and (self.problem.optimum is not None)
                    and ('nerror' in self.stop)):
                    cnt['nerror'] = -abs(self.fbest - self.problem.optimum)
        self.dolog()


        ## draw final positions.
        self.drawfinalpositions()
        self.drawbest(self.xbest)

        return self.log



    def dolog(self):
        self.log.append({
            'assessmentcnt':
                self.problem.assessmentcnt(),
            'fbest':self.fbest})



    def iscontinue(self, cnt, stop):
        """ decide whether we should continue
        searching. """
        tf = True
        for key in stop:
            if cnt[key] > stop[key]:
                tf = False
                break
        return tf

    def updatex(self, xnew, fnew, i, isdraw = True):
        if np.array_equal(self.x[i], xnew):
            if self.warn_selfupdate:
                dprint('updatex: warning! you are updating the x to the exact '
                       'same value! There may be an error in your '
                       'algorithm logic. You think you are modifying the x, '
                       'but '
                       'it is not being modified.')
        if isdraw:
            self.drawpath(self.x[i], xnew, i)
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
        #### draw the movement of best,
        #### if conditions hold
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
        if self.isdraw:
            self._poscolors = []
            for _ in self.positions:
                color = tuple(np.random.uniform(
                    0, 1, (3,)).tolist())
                self._poscolors.append(color)
                wx.Yield()


    def drawbest(self, pos):
        if self.isdraw:
            self.problem.visualiser.drawposition(
                pos, color = self.bestcolor(),
                scale_factor = 5)
            wx.Yield()

    def drawfinalpositions(self):
        if self.isdraw:
            for i in xrange(self.n):
                self.problem.visualiser.drawposition(
                    self.positions[i],
                    color = self._poscolors[i])

                # let mlab interact with user
                wx.Yield()

    def drawpath(self, oldpos, newpos, idx):
        """ draw a path from old pos to new pos for
        the position idx """
        if self.isdraw:
            self.problem.visualiser.drawpath(oldpos, newpos,
                color = self._poscolors[idx], tube_radius = .3, opacity = .8)
            self.problem.visualiser.drawposition(newpos,
                color = self._poscolors[idx], line_width = 5)
            wx.Yield()

    def drawpathbest(self, oldpos, newpos):
        """ draw paths of the best."""
        if self.isdraw:
            self.problem.visualiser.drawpath(oldpos, newpos,
                color = self.bestcolor(), tube_radius = .3, opacity = .8)
            wx.Yield()
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

        # set true if this is a minimization problem
        self.minimize = False
        self.isdebug = False
        self.isdebugprintassessments = False

        # theoretical best value, or optimum,
        # for the problem
        self.optimum = None

        self.ndims = None

        self.fixboundsfun = FixBounds.to_edges

        self.tweakmethod = 'adaptmaxstep'
        self.tweaksubmethod = 'bucclosed'

        # probability of adding noise to an element in solution vector
        self.tweakprob = 0.10

        # method of stepping from x to x+v
        self.stepbymethod = 'adaptivenotsame'
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
        if np.array_equal(pos, f):
            raise Exception(str(self.tweakfun) + ' is supposed to change the '
                            'solution. But apparantly it can not :). '
                            'solution: ' + str(pos) + 'tweak:' + str(f))
        return f

    def tweakfun(self, apos, method = None, submethod = None):
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

        return pos

    def stepby(self, pos, step):
        t = self.stepbyfun(pos, step)
        f = self.fixposition(t)
        if np.array_equal(pos, f):
            raise Exception(str(self.tweakfun) + ' is could not change the '
                            'solution. baaad. solution was ' + str(pos) +
                            ' and step was ' + str(step))
        return f

    def stepbyfun(self, pos, step):

        if   self.stepbymethod == 'adaptivenotsame':
            while True:
                t = pos + step
                newpos = self.fixposition(t)
                if not(np.array_equal(pos, newpos)): break
                step = step * 2
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
        self.isanimate = True
        self.isplotconvergence = True
        self.convergenceplottype = 'semilogy'
        self.isdebug = False
        self.stop = {'assessmentcnt':20}
        self.ntrials = 2
        self.problemlist = None
        self.algorithmlist = None
        self.returntrials = True
        self.writetrials = False
        self.writedir = '../tmp/results'
        self.imdir = '../latex/graphics'
        self.sep = '____',
        self.dashes = [],
        self.exptime = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        self.tmpdir = os.getcwd() + '/../latex/tmp/'
        self.expdir = self.tmpdir + self.exptime
        self.ndims = None
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

                    log = self.runonce(algorithm, problem, trial)

                    trialinfo = dict(algorithm = algorithm, problem = problem,
                        trial = trial, log = log)

                    if self.returntrials:
                        results.append(trialinfo)
                    if self.writetrials:
                        self.write(trialinfo)
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



    def write(self, t):
        filename = self.sep.join(t['algorithm'].name, t['problem'].name,
            #str(t['trial'])
            uuid.uuid4()
            )
        with open(filename, 'wb') as fd:
            pickle.dump(t, fd)

    def read(self, filename):
        with open(filename, 'rb') as fd:
            return pickle.load(fd)


    def mergetrials(self, runs):
        merged = {'acnt':[], 'meanbest':[], 'stdbest':[]}
        ## merge the events in the logs
        event = []
        for runidx, result in enumerate(runs):
            for record in result['log']:
                event.append(
                    (record['assessmentcnt'], record['fbest'], runidx))

        ## sort events by assessmentcnt
        e = np.array(event)
        event = e[e[:, 0].argsort()]

        if self.isdebug:
            print('event list:\n(assessmentcnt, fbest, trial)')
            pp(event)

        # start bests as NaNs.
        bests = np.ones(len(runs)) * np.NAN

        for e in event :
            acnt, fbest, idx = e
            bests[idx] = fbest
            mean = bests.mean()
            std = bests.std()

            # skip until all runs start contributing to the statistics.
            if not(np.isnan(np.sum(bests))):
                merged['acnt'].append(acnt)
                merged['meanbest'].append(mean)
                merged['stdbest'].append(std)

        return merged


    def get_dash(self, i):
        """ get a dash style for i th line in a plot """

        ### prepare some nice dashes. First these will be used.
        dash = [  # no dash: a line
            [2, 2],  # points

            [8, 2],  # dashes
            [8, 2, 2, 2],  # dash point
            [8, 2, 2, 2, 2, 2],
            [8, 2, 2, 2, 2, 2, 2, 2],
            [8, 2, 2, 2, 2, 2, 2, 2, 2, 2],

            [8, 2, 8, 2, ],
            [8, 2, 8, 2, 2, 2],
            [8, 2, 8, 2, 2, 2, 2, 2],
            [8, 2, 8, 2, 2, 2, 2, 2, 2, 2],
            [8, 2, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2],

            [8, 2, 8, 2, 8, 2],
            [8, 2, 8, 2, 8, 2, 2, 2],
            [8, 2, 8, 2, 8, 2, 2, 2, 2, 2],
            [8, 2, 8, 2, 8, 2, 2, 2, 2, 2, 2, 2],
            [8, 2, 8, 2, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ]

        if i < len(dash):
            return dash[i]
        else:
            ### If there is no pre-styled dash for i, prepare one automatically
            space = [32, 4]
            zero = [8, 4]
            one = [2, 4]

            br = bin(i)

            dashes = []
            dashes.extend(space)
            for i, e in enumerate(br):
                if i > 1:
                    if int(e) > 0:
                        dashes.extend(one)
                    else:
                        dashes.extend(zero)

            return dashes





    def pairname(self, probname, algoname):
        return probname + '______' + algoname


    def report(self, results = None, group_by = 'algo'):
        #### group results by algorithms, problems, and algorithm-problem pairs

#        algos = collections.defaultdict(list)
#        probs = collections.defaultdict(list)
        self.merges = {}
        self.results = results
        self.algos = collections.OrderedDict()
        self.probs = collections.OrderedDict()
        self.trials = collections.defaultdict(list)
        for result in results:
            algoname = result['algorithm'].name
            probname = result['problem'].name
            trialname = self.pairname(probname, algoname)

#            algos[algoname].append(result)
#            probs[probname].append(result)^
            self.algos[algoname] = result['algorithm']
            self.probs[probname] = result['problem']
            self.trials[trialname].append(result)

        ## say we do 10 trials for each pair. We need to merge these 10 trials
        ## into a single line in graphs.
        for trialname in self.trials:
            self.merges[trialname] = self.mergetrials(self.trials[trialname])

        return self.report_results()



    def report_results(self):
        def savefigure(fig, figtype, name):
            filename = (self.expdir + '/' + figtype + '/' + name)
            mkdirfor(filename)
            fig.savefig(filename + '.pdf', bbox_inches = 'tight')
            fig.savefig(filename + '.png', bbox_inches = 'tight')

            print('Saved ' + filename)

        ## plot problem comparisons.
        for name in self.algos:
            fig = self.plot_convergence_probs(name)
            #fig.canvas.set_window_title(name)
            savefigure(fig, 'algorithm', name)

        ## plot algo comparisons.
        for name in self.probs:
            fig = self.plot_convergence_algos(name)
            #fig.canvas.set_window_title(name + ' ' + self.probs[name].info)
            savefigure(fig, 'problem', name)
            if self.probs[name].info is not None:
                savefigure(fig, 'problem', name + ' ' + self.probs[name].info)


    def plot_convergence_probs(self, algoname):
        print("in plot convergence probs")
        ## get algorithm:
        algorithm = self.algos[algoname]

        ### get a new figure and axis
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #plt.title(algoname)
        plt.xlabel('FES')
        plt.ylabel(r'$f*$')

        ### draw algorithms
        plotidx = -1
        for probname in self.probs:
            ## gather info
            plotidx += 1
            problem = self.probs[probname]
            pairname = self.pairname(probname, algoname)
            y = self.merges[pairname]['meanbest']
            x = self.merges[pairname]['acnt']
            stdbest = self.merges[pairname]['stdbest']

            ### negate best values if necessary
            if algorithm.minimize != problem.minimize:
                y = [-e for e in y]

            plotargs = {'label': probname,
                        'linewidth': 2,
                        'color': 'black',
                        'dashes': self.get_dash(plotidx)}

            if self.convergenceplottype == 'semilogy':
                ### if y has negative values, plot is more appropriate
                if np.any(y < 0):
                    self.convergenceplottype = 'plot'  #
                else:
                    plotargs['basey'] = 2
                    h, = ax.semilogy(x, y, '--', **plotargs)

            if self.convergenceplottype == 'plot':
                h, = ax.plot(x, y, '--', **plotargs)

        plt.legend(handlelength = 3)
        return fig



#        #### rearrange ylim
#        ylim = list(ax.get_ylim())
#        if ((problem.optimum is not None) and ('nerror' in self.stop)):
#            if problem.minimize:
#                ylim[0] = problem.optimum + (-(self.stop['nerror']))
#            else:
#                ylim[1] = problem.optimum - (-(self.stop['nerror']))
#        ax.set_ylim(ylim)




    def plot_convergence_algos(self, probname):
        print('in plot convergence algos')
        ## get problem:
        problem = self.probs[probname]

        ### get a new figure and axis
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #plt.title(probname)
        plt.xlabel('FES')
        plt.ylabel(r'$f*$')

        ### draw algorithms
        algoidx = -1
        for algoname in self.algos:
            ## gather info
            algoidx += 1
            algorithm = self.algos[algoname]
            pairname = self.pairname(probname, algoname)
            y = self.merges[pairname]['meanbest']
            x = self.merges[pairname]['acnt']
            stdbest = self.merges[pairname]['stdbest']

            ### negate best values if necessary
            if algorithm.minimize != problem.minimize:
                y = [-e for e in y]

            plotargs = {'label': algoname,
                        'linewidth': 2,
                        'color': 'black',
                        'dashes': self.get_dash(algoidx)}

            if self.convergenceplottype == 'semilogy':
                ### if y has negative values, plot is more appropriate
                if np.any(y < 0):
                    self.convergenceplottype = 'plot'  #
                else:
                    plotargs['basey'] = 2
                    h, = ax.semilogy(x, y, '--', **plotargs)

            if self.convergenceplottype == 'plot':
                h, = ax.plot(x, y, '--', **plotargs)

        plt.legend(handlelength = 3)



        #### rearrange ylim
        ylim = list(ax.get_ylim())
        if ((problem.optimum is not None) and ('nerror' in self.stop)):
            if problem.minimize:
                ylim[0] = problem.optimum + (-(self.stop['nerror']))
            else:
                ylim[1] = problem.optimum - (-(self.stop['nerror']))
        ax.set_ylim(ylim)

        return fig















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
