import numpy as np

from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.fixbound import fixbound2bound
from pymeta.utils.pymetautils import randin

# ref: wikipedia.com/Particle_swarm_optimization
class ParticleSwarmOptimization(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit
        
        self.w = 0.90  # # defaults
        self.psip = 0.10
        self.psig = 0.60
        self.maxstepdivisor = 70
        self.fixboundfun = fixbound2bound
        self.name = 'PSO'
        self.npositions = 30
        
        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user
                
    def search(self):
        # ## shorter names to make program easier to read
        vis = self.problem.visualiser
        f = self.problem.height
        x = self.positions  # name x is preferred in articles
        isdraw = self.isdraw
        fixbound = self.fixboundfun
        rand = np.random.uniform
        w = self.w
        psip = self.psip 
        psig = self.psig 

        # ## initialization
        
        maxstep = (self.problem.ub - self.problem.lb) / self.maxstepdivisor
        S = x.shape[0]  # number of particles and dimensions 
        v = np.array([randin(-maxstep, maxstep) for _ in xrange(S)])  # initial velocities of the particles
        p = x.copy()  # best known position of each particle. make a hard copy of x
        fp = np.array([f(pos) for pos in x])  # heights of best positions
        idx = fp.argmax()  # # best of the best values: global best value
        colors=[];
        bestcolor = (1,1,0)
        def drawbest(pos): vis.drawposition(pos,color=bestcolor,scale_factor=5)
        if self.isdraw:
            drawbest(p[idx])
            for pos in x: 
                color =tuple(np.random.uniform(0,1,(3,)).tolist()) ; print 'color',color
                colors.append(color)
                vis.drawposition(pos,color=color)
                
            
        # ## main loop
        bestpos = p[idx].copy()
        maxhei = fp[idx]
        iteration = 0
        while True:
            iteration = iteration + 1
            yield (bestpos, maxhei, iteration)  # give control to caller. It will log and decide whether to stop.
            for i in xrange(S):  # #for each particle  
                # #better names
                xi = x[i].copy() ;print 'xi',xi
                vi = v[i].copy() ;print 'vi',vi
                pi = p[i].copy() ;print 'pi',pi
                
                rp = rand(0, 1, xi.shape) ;print rp # # produce a new position
                rg = rand(0, 1, xi.shape) ;print rg
                vnew = vi * w + (pi - xi) * rp * psip + (bestpos - xi) * rg * psig ;print 'vnew',vnew # new velocity
                x[i] = fixbound(self.problem, self, xi + vnew)  # new position
                #x[i] = xi + vnew ;print 'x[i]',x[i]

                #x[i]=xi+vnew
                fxi = f(x[i])  ;print 'fxi',fxi # height of the new position
                v[i] = x[i] - xi ;print 'v[i]',v[i] # correct velocity

                if self.isdraw: 
                    if not np.all(np.equal(xi,x[i])):
                        vis.drawpath(xi, x[i],color=colors[i],tube_radius=.3,opacity=.8)  # draw the path

                if fxi > fp[i]:  # # update personal best
                    p[i] = x[i].copy()
                    fp[i] = fxi
                    if fxi > maxhei:  # #update global best
                        if self.isdraw:
                            #drawbest(x[i])
                            vis.drawpath(bestpos,x[i],color=bestcolor,tube_radius=1.5)
                        bestpos = x[i].copy()
                        maxhei  = fxi
                        
                        #print bestpos,maxhei,iteration
                        yield (bestpos, maxhei, iteration)  # give control to caller. It will log and decide whether to stop.

