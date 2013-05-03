import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class funvis:
	def __init__(self, problem=None):
		plt.ion()
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot(10*np.random.randn(100), 10*np.random.randn(100), 'o')
		ax.set_title('Using hypen instead of unicode minus')
		plt.show()

