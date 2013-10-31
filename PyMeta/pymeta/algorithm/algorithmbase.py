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
		self.stop = None  # 	{'time':0, 'fbest': float('inf'), 'yieldcnt':float('inf') }  # TODO: also add minavaragestep
		self.isdebug = False
		self.log = []
		self.maxstepdivisor = 100;
		self.minimize = False
		# self._poscolors = []  # a list of colors. it will be initialized by the system.

		# self.__dict__.update(**kwargs)

	def f( self, poslist ):

		# ## which will we be using? cost or quality
		if self.minimize:
			obf = self.problem.cost
		else:
			obf = self.problem.quality


		# ## get f and fixed positions
		if poslist.ndim == 1:
			xfix = self.problem.fixposition( self.problem.fixbounds( poslist ) )
			ffix = obf( poslist )
			return ( xfix, ffix )
		elif poslist.ndim == 2:
			xfix = np.empty_like( poslist )
			for i in xrange( poslist.shape[0] ):
				xfix[i] = self.problem.fixposition( self.problem.fixbounds( poslist[i] ) )
			ffix = np.array( [obf( pos ) for pos in xfix] )
			return ( xfix, ffix )



	def run( self ):

		# ## for deciding which value is better which to use? <= or =>?
		if self.minimize:
			self.isbetter = lambda new, old: new <= old
		else:
			self.isbetter = lambda new, old: new >= old

		# ## fix positions, also get their objective values
		self.x, self.fx = self.f( self.positions )
		self.positions = self.x

		# ## possibly needed info
		self.n = self.x.shape[0]  # number of positions
		self.d = self.x.shape[1]  # number of dimensions on each position

		# ## initialize some important holders
		bestidx = 0
		if self.minimize:
			bestidx = self.fx.argmin()
		else:
			bestidx = self.fx.argmax()
		self.xbest = self.x[bestidx].copy();  # best position
		self.fbest = self.fx[bestidx]  # best value: global best value

		self.maxstep = ( self.problem.ub - self.problem.lb ) / self.maxstepdivisor

		# ## prepares colors for each position
		self.prepareposcolors()

		# ## main loop
		self.problem.resetassessmentcnt()
		self.yieldcnt = 0;
		tstart = time.time()
		cnt = {'fbest': self.fbest, 'time':0, 'yieldcnt':0, 'assessmentcnt':0 }
		yielder = self.search()
		while self.iscontinue( cnt, self.stop ):
			self.yieldcnt += 1
			yielder.next()  # call the actual search function
			cnt = {'fbest':self.fbest, 'xbest':self.xbest, 'time':time.time() - tstart, 'yieldcnt':self.yieldcnt, 'assessmentcnt':self.problem.assessmentcnt()}
			self.log.append( cnt )

		# ## draw final positions. this also prepares colors for each position
		self.drawfinalpositions()
		self.drawbest( self.xbest )

		return cnt.copy()


	def iscontinue( self, cnt, stop ):
		""" decide whether we should continue searching. """
		tf = True
		for key in stop:
			if cnt[key] > stop[key]:
				tf = False
				break
		return tf

	def updatex( self, xnew, fnew, i ):
		self.drawpath( self.x[i], xnew, i )
		self.x[i] = xnew
		self.fx[i] = fnew

	def updatebest( self, xnew, fnew ):
		self.drawpathbest( self.xbest, xnew )
		self.xbest = xnew.copy()
		self.fbest = fnew

	def updateposnbest( self, xnew, fnew, i ):
		""" if xnew is better than x, update x. if xnew is better than xbest, update xbest."""
		if self.isbetter( fnew , self.fx[i] ):  # update position of this ascender
			self.updatex( xnew, fnew, i )

			if self.isbetter( fnew, self.fbest ):  # update global best
				self.updatebest( xnew, fnew )

################# start drawing related methods ###############################

	def bestcolor( self ):
		return ( 1, 1, 0 )


	def prepareposcolors( self ):
		if self.isdraw:
			self._poscolors = []
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


