import os
import sys
import pprint

#get directory of this file
filedir=os.path.dirname(os.path.realpath(__file__)); print filedir

#get into this files directory
os.chdir(filedir)

#add some directories to python path
sys.path.extend('../.. ../problem ../algorithm ../utils ../visualiser'.split()); print sys.path

#import problems and such
#import metapy
from metapy.problem.rastrigin import NegativeRastriginProblem; 
problem = NegativeRastriginProblem()


from hillclimbing import HillClimbingAlgorithm; 
algorithm = HillClimbingAlgorithm()



solution = algorithm.run(problem=problem, maxtime=2)
print 'solution:', solution, 'height:', problem.height(solution)

