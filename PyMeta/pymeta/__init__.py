import numpy as np

from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin

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


class FixBounds():
    """
    Namespace for static methods of fixing bounds
    """
    @staticmethod
    def to_edges(pos = None, lb = None, ub = None):
        """ out of bounds dimensions are moved
        to edges."""
        high = pos > ub
        low = pos < lb
        pos[high] = ub[high]
        pos[low] = lb[low]
        return pos

    @staticmethod
    def full_random(pos = None, lb = None, ub = None):
        high = pos > ub
        low = pos < lb
        if np.any(high) or np.any(low):
            pos = randin(lb, ub)
        return pos

    @staticmethod
    def exceeder_random(pos, lb, ub):
        """ assign random values only to the
        dimensions that are out of bounds """

        high = pos > ub
        low = pos < lb
        hl = high | low
        if np.any(hl):
            pos[hl] = randin(lb[hl], ub[hl])

        return pos

if __name__ == '__main__':

    for f in [
              FixBounds.to_edges,
              FixBounds.full_random,
              FixBounds.exceeder_random,
              ]:

        pos = np.array([1, -3, 5, -7, 9, -11]).astype(float)
        ub = np.ones_like(pos) * 5
        lb = np.zeros_like(pos)
        print(f(pos, lb, ub))

    import inspect

    print 1
    print 1





















