import numpy as np
import pprint


from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.fixbound import fixbound2bound
from pymeta.utils.pymetautils import randin



# ref: wikipedia.com/Particle_swarm_optimization
class ParticleSwarmOptimization(OptimizationAlgorithm):
    # #list of class attributes
    w = None
    psip = None
    psig = None
    maxstepdivisor = None
    fixboundfun = None
    name = None
    npositions = None
    
    def __init__(self, **kwargs):
        # # defaults
        self.w = 0.90
        self.psip = 0.10
        self.psig = 0.60
        self.maxstepdivisor = 70
        self.fixboundfun = fixbound2bound
        self.name = 'PSO'
        self.npositions = 30
       
        self.__dict__.update(**kwargs)  # # overwrite defaults with keyword arguments supplied by user
        
        
        
    def search(self):
        vis = self.problem.visualiser  # #shorter names
        f = self.problem.height
        x = self.positions  # name x is preferred in articles
        isdraw = self.isdraw
        fixbound = self.fixboundfun
        rand = np.random.uniform
        w = self.w
        psip = self.psip 
        psig = self.psig 

        if isdraw: vis.pathcolor = rand(0, 1, (1, 3)) #set a random path color
        maxstep = (self.problem.ub - self.problem.lb) / self.maxstepdivisor
        S = x.shape[0]  # number of particles and dimensions 
        v = np.array([randin(-maxstep, maxstep) for _ in xrange(S)])  # initial velocities of the particles
        p = x.copy()  # best known position of each particle. make a hard copy of x
        fp = np.array([f(pos) for pos in x])  # heights of best positions
        idx = fp.argmax()  # # best of the best values: global best value
        bestpos = p[idx].copy()
        maxhei = fp[idx]
        iteration = 0;
        while self.iscontinue():
            print 'pso iteration', iteration
            for i in xrange(S):  # #for each particle  
                xi, vi, pi = x[i], v[i], p[i]  # #better names
                
                rp = rand(0, 1, xi.shape)  # # produce a new velocity
                rg = rand(0, 1, xi.shape)
                vnew = vi * w + (pi - xi) * rp * psip + (bestpos - xi) * rg * psig
                x[i] = fixbound(self.problem, self, xi + vnew)  # new position
                fxi = f(x[i])  # height of the new position
                v[i] = x[i] - xi  # correct velocity

                if isdraw: vis.drawpath(xi, x[i])  # # visualise
                
                if fxi > fp[i]:  # # update personal best
                    p[i] = x[i].copy()
                    fp[i] = fxi
                    if fxi > maxhei:  # #update global best
                        bestpos = x[i].copy()
                        maxhei = fxi
                        bestpos, maxhei = self.bookkeep(bestpos, maxhei, iteration)
        
            
            bestpos, maxhei = self.bookkeep(bestpos, maxhei, iteration)
            iteration = iteration + 1
            
        if isdraw: vis.drawbest(bestpos)
            
        return(bestpos, maxhei)
    
    