import time
from pymeta.utils.pymetautils import Default

import wx

class OptimizationAlgorithm(Default):
	def __init__(self):
		Default.__init__(self)

		self.name = '?'
		self.problem = None;
		self.positions = None;
		self.stop= None #	{'time':0, 'maxhei': float('inf'), 'iteration':float('inf') }  # TODO: also add minavaragestep
		self.debug = False
		self.log =[]
		#self.__dict__.update(**kwargs)
		
	def run(self):
		
		tstart = time.time()	
	
		cnt = {'time':0, 'maxhei': float('-inf'), 'iteration':0, 'assessmentcnt':0 }
		loop = self.search()  # call the actual search function
		while self.iscontinue(cnt,self.stop):
			bestpos, maxhei, iteration = loop.next()
			cnt={'time':time.time()-tstart,	'iteration':iteration,'maxhei':maxhei,'bestpos':bestpos,'assessmentcnt':self.problem.assessmentcnt()}
			print "yield:",cnt
			self.log.append(cnt)
			if self.isdraw:
				wx.Yield() #let wx interact with user
			#if self.isdraw and run_draw, draw a path between old and new positions of the changed positions.

		if self.isdraw: self.problem.visualiser.drawbest(bestpos)

		return cnt.copy()
						
	
	def iscontinue(self,cnt,stop):
		tf = True
		for key in stop:
			if cnt[key] > stop[key]:
				tf = False
				break
		return tf
	
	
