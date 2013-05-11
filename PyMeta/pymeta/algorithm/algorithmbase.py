import time
from pymeta.utils.pymetautils import Default

class OptimizationAlgorithm(Default):
	name = '?'
	problem = []
	isdraw = False
	#hasrunner = False
	#isrunner = False
	
	positions = []
	npositions = 1
	
	# fixboundsfun = fixbound2bound
	# selectfun = tournamentselection
	# neg2posfun = 
	
	cnt  = {'time':0, 'bestheight': float('-inf'), 'iteration':0 }
	stop = {'time':0, 'bestheight': float('inf'), 'iteration':float('inf') }  # TODO: also add minavaragestep
	
	log = []
	tstart = time.time()
	#iteration = 0
	bestheight = float('-inf')
	
	debug = False
		
	def run(self):
		tstartt = time.time()
		position, height = self.search()  # call the actual search function
		others = {}  # # book keeping stuff
		others['algorithm'] = self  
		others['runcnt'] = 1
		others['timecnt'] = time.time() - tstartt
		others['timeavg'] = others['timecnt'];
		self.positions[0] = position  # overwrite positions[0]
		return (position, height, others)
								
	def bookkeep(self, bestpos, bestheight, iteration):
		self.cnt['time'] = time.time() - self.tstart  # # update cnt
		self.cnt['iteration'] = iteration
		self.cnt['bestheight'] = bestheight
		self.cnt['bestpos'] = bestpos
		self.log.append(self.cnt.copy())  # update log
		self.bestheight = bestheight  # update self.bestheight
		if self.debug:
			print 'best:', self.cnt
		return (bestpos, bestheight)
	
	def iscontinue(self):
		tf = True
		for key in self.stop:
			if self.cnt[key] > self.stop[key]:
				tf = False
				break
		return tf
	
	
