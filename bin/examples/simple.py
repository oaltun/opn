#-*- coding: utf-8 -*-
from __future__ import division

def main():
	# DO NECESSARY IMPORTS------------------------------------
	# Arrangements for using pyqt4 as backend
	import sip
	sip.setapi('QString', 2)
	sip.setapi('QVariant', 2)
	import matplotlib
	matplotlib.use('qt4agg')
	
	# Import necessary libraries
	import matplotlib.pyplot as plt		
	import os, sys
	from pprint import pprint
	import numpy as np
	
	# Change working directory to the directory of this script
	filedir = os.path.dirname(os.path.realpath(__file__))
	print "Starting in directory below:\n", filedir, "\n"
	os.chdir(filedir)
	
	# Arrange paths for importing opn	
	import sys
	path_to_opn = '../..'
	sys.path.extend(['.',path_to_opn])	
	
	# Import opn
	print("Importing opn")
	import opn as pm
	from opn.problem import benchmark
	from opn.algorithm import pso
	print("Imported opn")
	print('')

	
	# SET OPTIONS----------------------------------------------------
	
	# Visualise? Visualisation is available for problems of two dimensions on real domain.
	isdraw = False 
	
	# Draw solution updates?
	isdrawupdatex = isdraw 

	# After how many function evaluations (FES, assessments) should the algorithm stop? 
	stop ={'assessmentcnt':1000}

	# PREPARE THE PROBLEM TO BE SOLVED---------------------------------

	# The 'benchmark' module has some classical test problems. The dimensionality is inferred from the ub (upper bounds) or lb (lower bounds)
	ub=np.array([5,5])
	lb = -ub
	problem = benchmark.RastriginProblem(ub=ub,lb=lb)


	# PREPARE THE ALGORITHM TO BE USED----------------------------------

	algorithm = pso.ParticleSwarmOptimization(
		  name='PSO',
		  problem=problem,
		  stop=stop,
		  npositions=30, #how many solutions (particles, chromosomes) should the algorithm use?
		  isdraw=isdraw,
		  isdrawupdatex=isdrawupdatex
		  )

	# GIVE STARTING POSITIONS OF PARTICLES
	algorithm.positions = problem.randposn(algorithm.npositions)

	# PREPARE VISUALISER TO BE USED-------------------------------------
	if isdraw:
		#also try pm.TwoDFunVisualiserColor 
		problem.visualiser = pm.TwoDFunVisualiser3D(
			problem=problem,
			title = problem.name + ' - ' + algorithm.name
			)
		problem.visualiser.init()

	# RUN THE ALGORITHM-----------------------------------------------------
	algorithm.run()

	# EXTRACT INFORMATION FROM THE ALGORITHM AND REPORT --------------------
	# algorithm.logfes has the function evaluation numbers that globals best (fbest) changes.
	# algorithm.logfbest has the corresponding new global best values.
	# algorithm.xbest has the current best solution. Hence, when the main loop of the algorithm terminate, it has the last best solution.
	print('')
	print('(FES, FBEST):')
	pprint(zip(algorithm.logfes,algorithm.logfbest))
	print('')
	print('XBEST:')
	print(algorithm.xbest)

	if isdraw:
		plt.show()



if __name__ == '__main__':
	main()
