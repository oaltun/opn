#-*- coding: utf-8 -*-
from __future__ import division

# SETTINGS FOR IMPORTS:

# Path to the directory that (lowercase) 'pymeta' directory resides in.
# It can be absolute or relative.
path_to_pymeta = '../../../../opn/PyMeta'


# END SETTINGS FOR IMPORTS

# IMPORTS
# Import non-pymeta libraries.

import os, sys
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	# Arrange paths for importing pymeta
	filedir = os.path.dirname(os.path.realpath(__file__))
	print "Starting in directory below:\n", filedir, "\n"
	os.chdir(filedir)
	sys.path.extend(['.',path_to_pymeta])



	print("Importing pymeta")
	import pymeta as pm
	from pymeta.problem import benchmark
	from pymeta.algorithm import pso
	print("Imported pymeta")
	print('')
	#---MAIN---

	#OPTIONS

	isdraw = False # Visualise? Visualisation is available for problems of two dimensions on real domain.
	isdrawupdatex = isdraw # Draw solution updates?

	# After how many function evaluations (FES, assessments) should the algorithm stop? 
	stop ={'assessmentcnt':1000}

	# PREPARE THE PROBLEM  TO BE SOLVED:

	# The 'benchmark' module has some classical test problems:

	ub=np.array([5,5])
	lb = -ub
	problem = benchmark.RastriginProblem(ub=ub,lb=lb)


	# PREPARE THE ALGORITHM

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

	# ARRANGE VISUALISATION
	if isdraw:
		#also try pm.TwoDFunVisualiserColor 
		problem.visualiser = pm.TwoDFunVisualiser3D(
			problem=problem,
			title = problem.name + ' - ' + algorithm.name
			)
		problem.visualiser.init()

	# RUN THE ALGORITHM
	algorithm.run()

	# EXTRACT INFORMATION FROM THE ALGORITHM
	# algorithm.logfes has the function evaluation numbers that globals best (fbest) changes.
	# algorithm.logfbest has the corresponding new global best values.
	# algorithm.xbest has the current best solution. Hence, when the main loop of the algorithm terminate, it has the last best solution.
	print('')
	print('(FES, FBEST):')
	pprint(zip(algorithm.logfes,algorithm.logfbest))
	print('')
	print('XBEST:')
	print(algorithm.xbest)

	# SHOW PLOTS
	if isdraw:
		plt.show()


