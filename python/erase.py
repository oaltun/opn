import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
x = np.random.random(2)
y = np.random.random(2)
z = np.random.random(2)
ax.plot(x, y, z, label='parametric curve')
ax.legend()
print 1
plt.show()
print 2
