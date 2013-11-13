from pymeta.utils.pymetautils import randin, Default
import numpy as np
class GenericOptimizationProblem(Default):
    def __init__(self, **kwargs):
        Default.__init__(self)  # inherit
        # self.heightfun = None; ##defaults
        self.lb = None
        self.ub = None
        self.name = None
        self.visualiser = None
        self.minimize = False  # set true if this is a minimization problem
        self.isdebug = False
        self.__dict__.update(**kwargs)  # overwrite

        self._assessmentcnt = 0

    def setdims(self, dim):
        self.ub = np.ones(dim) * self.ub[0]
        self.lb = np.ones(dim) * self.lb[0]
        self.name = self.name + ('(Dims=%d)' % dim)

    def dims(self):
        return len(self.ub)

    def assessmentcnt(self):
        return self._assessmentcnt

    def resetassessmentcnt(self):
        self._assessmentcnt = 0

    def quality(self, position):
        return self.height(position)

    def height(self, position):

        h = self.heightfun(position)
        self._assessmentcnt = self._assessmentcnt + 1;
        if self.isdebug:
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

    def tweak(self, pos, maxstep):
        return pos + randin(-maxstep, maxstep)

    def pos2str(self, pos):
        return str(pos)

    def fixposition(self, pos):
        """fix problems about position: invalid, etc."""
        return pos

    def fixbounds(self, pos):
        """fix out of boundary situation"""
        high = pos > self.ub
        low = pos < self.lb
        pos[high] = self.ub[high]
        pos[low] = self.lb[low]
        return pos
