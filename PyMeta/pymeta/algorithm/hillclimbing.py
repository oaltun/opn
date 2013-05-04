#reference: Essentials of Metaheuristics by Sean Luke
#Steepest Ascent Hill-Climbing Algorithm 
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin
import time


import numpy

class HillClimbingAlgorithm(OptimizationAlgorithm):
	"""Hill Climbing Algorithm variant"""
	
	def __init__(self,ntweaks=8,maxstepdivisor=100):
		self.ntweaks = ntweaks
		self.maxstepdivisor = maxstepdivisor
		
	def run(self, 
		problem=None, 
		initialx=None, 
		visualiser=None, 
		maxiter=numpy.inf, 
		maxtime=numpy.inf, 
		maxquality=numpy.inf ):
		"""compulsary function that will implement the algorithm."""
		
		def tweak(current):
			"""an inner function to tweak the current solution"""
			l = numpy.nanmax(numpy.array([problem.lb, current-maxstep]), axis=0) #lower bound to for new random solution: maximum of problems lower bound and curent position minus maxstep. this way we are sure to produce in bounds values.
			u = numpy.nanmin(numpy.array([problem.ub, current+maxstep]), axis=0)
			return randin(l,u)
			
		
		## some options and 
		maxstep = (problem.ub-problem.lb)/self.maxstepdivisor
		maxes = numpy.array([maxiter, maxtime, maxquality])
			
		## init values before entering main loop
		S = initialx or randin(problem.lb,problem.ub) #start point given by the user or some initial candidate solution
		best = problem.height(S)
		itercnt = 0
		timecnt = 0
		starttime = time.time()
		
		#main loop: while we did not do enough iterations, and we did not fill our time, and we did not reach maxquality, do:
		while numpy.all(numpy.array([itercnt, timecnt, best]) <= maxes):
			
			## check n tweaks, or neighbors and get the best
			R = tweak(S)
			for i in range(self.ntweaks-1):
				W = tweak(S)
				if problem.height(W)>problem.height(R):
					R = W
					
			#do we need to change our place?
			if problem.height(R) > problem.height(S):
				S = R
				best = problem.height(R)
				
				if visualiser:
					visualiser.drawpath(R,S)
				
			#book keeping:
			itercnt=itercnt+1
			timecnt=time.time()-starttime
			print itercnt,timecnt,S,best
			
		#return the solution found
		return S
			
