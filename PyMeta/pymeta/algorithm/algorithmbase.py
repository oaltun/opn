import time
from pymeta.utils.pymetautils import Default
import numpy as np

import wx

class OptimizationAlgorithm( Default ):
	def __init__( self ):
		Default.__init__( self )

		self.name = '?'
		self.problem = None
		self.positions = None
		self.npositions = 20
		self.stop = None  # 	{'time':0, 'fbest': float('inf'), 'iteration':float('inf') }  # TODO: also add minavaragestep
		self.debug = False
		self.log = []
		self.maxstepdivisor = 100;
		self.minimize = False
		self._poscolors = []  # a list of colors. it will be initialized by the system.

		# self.__dict__.update(**kwargs)

	def run( self ):

		# ## start value for fbest changes according to problem type
		if self.problem.minimize:
			bestf = float( 'inf' )
		else:
			bestf = float( '-inf' )

		# ## whether we use cost or height changes according to problem type
		if self.minimize:
			self.f = self.problem.cost  # if minimization algorithm, use cost
		else:
			self.f = self.problem.quality  # if maximization algorithm, use quality

		# ## for deciding which value is better which to use? <= or =>?
		if self.minimize:
			self.isbetter = lambda new, old: new <= old
		else:
			self.isbetter = lambda new, old: new >= old

		# ## better names
		self.x = self.positions  # positions are given name x in papers

		# ## possibly needed info
		self.n = self.x.shape[0]  # number of positions
		self.d = self.x.shape[1]  # number of dimensions on each position

		# ## initialize some important holders
		self.xbest = self.x[0].copy();  # best position
		self.fbest = self.f( self.xbest )  # best value: global best value
		self.fx = np.array( [self.f( pos ) for pos in self.x] )  # value of all positions

		self.maxstep = ( self.problem.ub - self.problem.lb ) / self.maxstepdivisor

		# ## prepares colors for each position
		self.prepareposcolors()


		# ## main loop
		self.problem.resetassessmentcnt()
		self.iteration = 0;
		tstart = time.time()
		cnt = {'time':0, 'fbest': bestf, 'iteration':0, 'assessmentcnt':0 }
		loop = self.search()
		while self.iscontinue( cnt, self.stop ):
			self.iteration += 1
			bestx, bestf, iteration = loop.next()  # call the actual search function
			cnt = {'time':time.time() - tstart, 'iteration':iteration, 'fbest':bestf, 'xbest':bestx, 'assessmentcnt':self.problem.assessmentcnt()}
			self.log.append( cnt )

		# ## draw final positions. this also prepares colors for each position
		self.drawfinalpositions()
		self.drawbest( bestx )

		return cnt.copy()


	def iscontinue( self, cnt, stop ):
		""" decide whether we should continue searching. """
		tf = True
		for key in stop:
			if cnt[key] > stop[key]:
				tf = False
				break
		return tf

	def updateposnbest( self, xnew, fnew, i ):
		""" if xnew is better than x, update x. if xnew is better than xbest, update xbest."""
		if self.isbetter( fnew , self.fx[i] ):  # update position of this ascender
			self.drawpath( self.x[i], xnew, i )
			self.x[i] = xnew
			self.fx[i] = fnew

			if self.isbetter( fnew, self.fbest ):  # update global best
				self.drawpathbest( self.xbest, xnew )
				self.xbest = xnew.copy()
				self.fbest = fnew

################# start drawing related methods ###############################

	def bestcolor( self ):
		return ( 1, 1, 0 )


	def prepareposcolors( self ):
		if self.isdraw:
			for _ in self.positions:
				color = tuple( np.random.uniform( 0, 1, ( 3, ) ).tolist() )
				self._poscolors.append( color )
				wx.Yield()


	def drawbest( self, pos ):
		if self.isdraw:
			self.problem.visualiser.drawposition( pos, color = self.bestcolor(), scale_factor = 5 )
			wx.Yield()

	def drawfinalpositions( self ):
		if self.isdraw:
			for i in xrange( self.n ):
				self.problem.visualiser.drawposition( self.positions[i], color = self._poscolors[i] )
				wx.Yield()  # let mlab interact with user

	def drawpath( self, oldpos, newpos, idx ):
		""" draw a path from old pos to new pos for the position idx """
		if self.isdraw:
			self.problem.visualiser.drawpath( oldpos, newpos, color = self._poscolors[idx], tube_radius = .3, opacity = .8 )  # draw the path;
			wx.Yield()

	def drawpathbest( self, oldpos, newpos ):
		""" draw paths of the best."""
		if self.isdraw:
			self.problem.visualiser.drawpath( oldpos, newpos, color = self.bestcolor(), tube_radius = .3, opacity = .8 )  # draw the path;
			wx.Yield()
######################### end drawing related methods #########################


