from __future__ import division
from pymeta.utils.pymetautils import Default
import numpy as np
from pymeta.utils.pymetautils import randin
import wx

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
                if ((self.problem.optimum is not None)
                    and ('nerror' in self.stop)):
                    cnt['nerror'] = -abs(self.fbest - self.problem.optimum)
        self.dolog()


        ## draw final positions.
        self.drawfinalpositions()
        self.drawbest(self.xbest)


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

    def updatex(self, xnew, fnew, i):
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
            self.problem.visualiser.drawpath(
                oldpos, newpos,
                color = self._poscolors[idx],
                tube_radius = .3, opacity = .8)
            self.problem.visualiser.drawposition(
                newpos, color = self._poscolors[idx],
                line_width = 5)
            wx.Yield()

    def drawpathbest(self, oldpos, newpos):
        """ draw paths of the best."""
        if self.isdraw:
            self.problem.visualiser.drawpath(
                oldpos, newpos,
                color = self.bestcolor(),
                tube_radius = .3,
                opacity = .8)  # draw the path;
            wx.Yield()
###end drawing related methods ###
