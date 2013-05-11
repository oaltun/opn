import numpy
def fixbound2bound(problem,algorithm,pos):
    high=pos>problem.ub
    low = pos<problem.lb
    pos[high]=problem.ub[high]
    pos[low] =problem.lb[low]
    return pos
    
if __name__ == '__main__':
    print 'start'
    from problem.rastrigin import NegativeRastriginProblem
    problem=NegativeRastriginProblem();
    print problem
    pos=numpy.array([1,-6])
    fixbound2bound(problem,[],pos)
    print pos