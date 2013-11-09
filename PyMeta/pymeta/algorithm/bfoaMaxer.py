
import numpy as np
from pymeta.algorithm.algorithmbase import OptimizationAlgorithm
from pymeta.utils.pymetautils import randin
import matplotlib.pyplot as plt

####################################################################################
def compute_cell_interact( d, w, cells, i ):
    s = 0.0
    diff = 0.0
    for other in xrange( len( cells ) ):
        if i != other:
            diff = np.sum( ( cells[i] - cells[other] ) ** 2 )
            s += d * np.exp( w * diff )
    return s

#####################################################################################
class BacterialForagingOptimizationAlgoritm2( OptimizationAlgorithm ):
    def __init__( self, **kwargs ):

        OptimizationAlgorithm.__init__( self )  # inherit

        self.npositions = 50  # Total number of bacteria in the population
        self.Ned = 2  # Number of elimination-dispersal steps
        self.Nc = 70  # Number of chemotaxis steps
        self.Ns = 4  # The swimming length
        self.Nre = 4  # The number of reproduction steps
        self.Ped = 0.25  # Elimination-dispersal probability
        self.Ci = 0.1  # Step size
        self.maxstepdivisor = 70
        self.d_attr = -0.1
        self.w_attr = -0.2
        self.h_rep = 0.1
        self.w_rep = -10

        self.__dict__.update( **kwargs )

    def search( self ):

        vis = self.problem.visualiser
        cost = self.problem.cost
        cells = self.positions
        isdraw = self.isdraw
        rand = np.random.uniform
        Ned = self.Ned; Nc = self.Nc; Ns = self.Ns; Nre = self.Nre; Ped = self.Ped; bestpos = self.bestpos

        ### Initialization ####

        self.maxstep = ( self.problem.ub - self.problem.lb ) / self.maxstepdivisor
        S = cells.shape[0]
        costc = np.array( [cost( pos ) for pos in cells] )  # the cost of the positions
        healthc = costc.copy()
        idbest = costc.argmin()  # the index of the more healthy position


        colors = [];
        bestcolor = ( 1, 1, 0 )
        def drawbest( pos ): vis.drawposition( pos, color = bestcolor, scale_factor = 5 )
        if self.isdraw:
            drawbest( cells[idbest] )
            for pos in cells:
                color = tuple( np.random.uniform( 0, 1, ( 3, ) ).tolist() ) ; print 'color', color
                colors.append( color )
                vis.drawposition( pos, color = color )

        bestpos = cells[idbest].copy()
#         print 'Best position of the cells is .....' , bestpos;
        maxhei = costc[idbest]
#         print 'Min cost of the position at the beginning is.... ', maxhei;
        iteration = 0
        r = []
        while True:
            yield ( bestpos, maxhei, iteration )  # give control to caller. It will log and decide whether to stop.
            if iteration > 3:
                z = range( iteration )
                plt.plot( r, 'r-' )
                plt.title( 'Negative Rastrigin with Genetic Algorithm ' )
                plt.xlabel( 'Iterations' )
                plt.ylabel( 'Fitness' )
                plt.show()
            iteration = iteration + 1
            print 'Iteration is : .............. : ', iteration

            for l in xrange( Ned ):
                for k in xrange( Nre ):
                    c_best = None
                    for j in xrange( Nc ):
                        c_best, cells, costc, healthc = self.chemotaxis( c_best, cells, costc, healthc, j )



                        if bestpos == None or self.problem.height( c_best ) > self.problem.height( bestpos ):
                            bestpos = c_best
                    # # The best of each chemotaxis step
                    print 'The best cost : ', cost( bestpos )
                    # # Sort by Cell Health ascending order(Increasing)
                    # #order = np.argsort(healthc)
                    # #cells = cells[order]
                    cells = [x for ( y, x ) in sorted( zip( healthc, cells ), reverse = False )]  # # healthc == sum_nutrients
                    ### Selection : first best healthy doubled ###
                    '''Reproduction: The least healthy bacteria eventually die while each of the healthier bacteria (those
                        yielding lower value of the objective function) asexually split into two bacteria, which are then
                        placed in the same location. This keeps the swarm size constant.'''
                    cells = cells[:S / 2] + cells[:S / 2]

                    # ## Create cell at random Location
                '''Eliminate and disperse each bacterium, which results in in keeping the number
                of bacteria in the population constant.'''
                for i in xrange( len( cells ) ):
                    if rand() <= Ped:
                        cells[i] = randin( -self.maxstep, self.maxstep )
            ### After each iteration ###
#             costc = np.array([cost(pos) for pos in cells])
#             idbest = costc.argmax()
#             if costc[idbest] > maxhei:
#                 if self.isdraw:
#                     #drawbest(x[i])
#                     vis.drawpath(bestpos,cells[idbest],color=bestcolor,tube_radius=1.5)
#                     bestpos = costc[idbest].copy()
#                     maxhei  = costc[idbest]
#                     r.append(maxhei)
#                     print 'Maximum fitness is :............................:', maxhei
#                     print 'Best position is ...............................:',cells[idbest]


    # # For computing the attraction and repelsion of the cells
    def compute_inter( self, cells, i ):
        attract = compute_cell_interact( self.d_attr, self.w_attr, cells, i )
        repel = compute_cell_interact( self.h_rep, self.w_rep, cells, i )
        inter = attract + repel
        return inter
    ###########################################################
    # # Chemotaxis steps ( Swimming and Tumbling )
    def chemotaxis( self, c_best, cells, costc, healthc, j ):
        for i in xrange( len( cells ) ):
            ### To-Do : Each bac. moves simultaneously ####
            sum_nutrients = 0.0
            # # Cost,Fitness(Health) of cells before moving to another location
            inter = self.compute_inter( cells, i )  # # interaction before tumbling.
            c = self.problem.height( cells[i] )  # # cost before tumbling.
            costc[i] = c
            fitness = c + inter
            healthc[i] = fitness
            if c_best == None or costc[i] > self.problem.height( c_best ):
                c_best = cells[i].copy()
            sum_nutrients += healthc[i]
            for m in xrange( self.Ns ):
                step = randin( -self.maxstep, self.maxstep )  # # Tumbled cells


                newcell = cells[i] + step
                if self.isdraw:
                    self.problem.visualiser.drawpath()


                cells[i] = newcell
                inter = self.compute_inter( cells, i )  # # interaction while swimming.
                c = self.problem.height( cells[i] )
                costc[i] = c
                newfitness = c + inter
                if costc[i] > self.problem.height( c_best ):
                    c_best = cells[i].copy()
                if newfitness < fitness:
                    break
                else:
                    '''The bacterium changes its position only if the modified objective function
                        value is less than the previous one'''
                    cells[i] = newcell
                    fitness = newfitness
                    healthc[i] += newfitness  # # healthc = sum_nutrients
                    costc[i] = c
        print 'chemotaxis ', j, ' f = ', min( healthc ), 'cost = ', self.problem.height( c_best )
        return c_best, cells, costc, healthc

    ###########################################################





























