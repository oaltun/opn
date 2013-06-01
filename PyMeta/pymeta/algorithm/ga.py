import numpy as np
from numpy import *
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.fixbound import fixbound2bound
from pymeta.utils.pymetautils import randin
import matplotlib.pyplot as plt

class GeneticAlgorithm(OptimizationAlgorithm):
    def __init__(self, **kwargs):
        OptimizationAlgorithm.__init__(self)  # inherit
        
        self.mutate = 0.1  # # for two dimensional problems mutation probability should be chosen high, otherwise you might stuck in a local maximum.
        self.random_select = 0.05
        self.retain = 0.2
        self.pcrossover=0.5
        self.maxstepdivisor = 70
        self.fixboundfun = fixbound2bound
        self.name = 'GA'
        self.npositions = 50
        self.__dict__.update(**kwargs)  # overwrite defaults with keyword arguments supplied by user
                
    def search(self):
        # ## shorter names to make program easier to read
        vis = self.problem.visualiser
        f = self.problem.height
        x = self.positions  # name x is preferred in articles
        isdraw = self.isdraw
        fixbound = self.fixboundfun
        rand = np.random.uniform
        mutate = self.mutate
        random_select = self.random_select
        retain = self.retain 
        ub = self.problem.ub
        lb = self.problem.lb
        # ## initialization
        
        maxstep = (self.problem.ub - self.problem.lb) / self.maxstepdivisor
        S = x.shape[0]  # number of particles and dimensions 
        fx = np.array([f(pos) for pos in x])  # heights of best positions
        idx = fx.argmax()  # # best of the best values: global best value
        colors = [];
        bestcolor = (1, 1, 0)
        def drawbest(pos): vis.drawposition(pos, color=bestcolor, scale_factor=5)
        if self.isdraw:
            drawbest(x[idx])
            for pos in x: 
                color = tuple(rand(0, 1, (3,)).tolist()) ; print 'color', color
                colors.append(color)
                vis.drawposition(pos, color=color)
                
        print 'Maximum fitnets at the begining ............................:',max(fx)
      
             
#  GA ALGORITHM STARTS HERE................................

        bestpos = x[idx].copy()
        print 'Best position is ...............',x[idx]
        maxhei = fx[idx]
        iteration = 0
        r=[]
        while True:
#             fx=np.array([f(pos) for pos in x])
#             idx=fx.argmax()
#             maxhei=fx[idx]
#             print 'Maximum fitness is :............................:', maxhei
#             print 'Best position is ...............................:',x[idx]
            iteration = iteration + 1;print 'ITERATION IS :.......................:',iteration
            yield (bestpos, maxhei, iteration)  # give control to caller. It will log and decide whether to stop.
            if iteration>999:
                z=arange(iteration)
                plt.plot(r,'r-')
                plt.title('Negative Rastrigin with Genetic Algorithm ')
                plt.xlabel('Iterations')
                plt.ylabel('Fitness')
                plt.show()
                
            order = np.argsort(fx)[::-1]
            
#   SELECTION :"ELITISM" method has been used for selecting next generation. 
            retain_length = int(S * retain)
            x = x[order]
            parents = x[:retain_length]
            for row in x[retain_length:]:
                if random_select > rand(0, 1, 1):
                    parents = np.vstack(parents)  
            
       
#   RECOMBINATION   :"SINGLE POINT CROSSOVER" method used.                       
            nparents=parents.shape[0]
            nchild=S-nparents
                        
            def crossover(male,female):
                child1=male.copy()
                child2= female.copy()
                for i in xrange(male.size):
                    if np.random.uniform(0,1,1)>self.pcrossover:
                        temp=child1[i]
                        child1[i]=child2[i]
                        child2[i]=temp            
                return (child1, child2)
                                    
            children=[]
            while len(children)<nchild:
                inxparent1=np.random.randint(nparents)
                inxparent2=np.random.randint(nparents)
                if inxparent1!=inxparent2:
                    child1,child2=crossover(parents[inxparent1],parents[inxparent2])
                    children.append(child1)
                    children.append(child2)
            while len(children)>nchild:
                del children[-1]            
            x=vstack((parents,children))
           # print 'before mutation.........',x
 
#   MUTATION  :Mutates recombined individuals.
#           
            for ind in x:
                if mutate > np.random.uniform(0, 1, 1):
                    elem_to_mutate = np.random.randint(ind.size)
                    ind[elem_to_mutate] = rand(self.problem.lb[elem_to_mutate], self.problem.ub[elem_to_mutate], 1)
          #  print 'after mutation...........',x          
            
            fx=np.array([f(pos) for pos in x])
            idx=fx.argmax()
            if fx[idx]>maxhei:
                if self.isdraw:
                            #drawbest(x[i])
                            vis.drawpath(bestpos,x[idx],color=bestcolor,tube_radius=1.5)
                bestpos = x[idx].copy()
                maxhei  = fx[idx]
            r.append(maxhei)
            print 'Maximum fitness is :............................:', maxhei
            print 'Best position is ...............................:',x[idx]
            
        
       

           
           
           
           
           
       
                
                
                
                            

