import rastrigin
import hillclimbing
import funvis

problem = rastrigin.rastrigin()
algorithm = hillclimbing.hillclimbing()
visualiser= funvis.funvis(problem)
solution = algorithm.run(problem=problem, maxtime=2)
print 'solution:', solution, 'quality:', problem.quality(solution)

raw_input('press enter to exit')