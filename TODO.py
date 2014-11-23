# TODO: use prng's instead of global random number generator. 
# See http://stackoverflow.com/questions/5836335/consistenly-create-same-random-numpy-array/5837352#5837352

# TODO: installation using distutils. get rid of need to adjust paths in the main programs.

# TODO: add unittests 

# TODO: code needs a lot of documentation

# TODO: divide 'OptimizationAlgorithm' base class into two: OneTrial and 'AlgorithmBase'.
#    The stuff in the OptimizationAlgorithm.run() should be in OneTrial

# TODO: rename 'assessmentcnt' to 'fes'

# TODO: remove self.problem.tweak(), get rid of self.tweakfun() and self.subtweakfun() . the users 
#    should call explicit tweak_bucclosed, etc. Gather all tweak functions in a file called tweak.py

# TODO: remove isbetterORequal and isbetterNOTequal

# TODO: remove calls to dict.update() in __init__() methods.

# TODO: pep 8? conformance(e.g. Naming style )

# TODO: for 3d visualisation, move from mayavi to matplotlib. So that we can move to Python 3.

# TODO: better messages (serious) in "raise Exception" statements

# TODO: get rid of stepby() method.