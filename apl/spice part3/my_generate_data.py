# script to generate data files for the least squares assignment
from pylab import *
import scipy.special as sp
from numpy import *
import matplotlib.pyplot as plt
N=101                           # no of data points
k=9                             # no of sets of data with varying noise

# generate the data points and add noise
t=linspace(0,10,N)                       # t vector
y=1.05*sp.jn(2,t)-0.105*t            # f(t) vector
Y=meshgrid(y,ones(k),indexing='ij')[0]                      # make k copies
scl=logspace(-1,-3,k)    
n=dot(random.randn(N,k),diag(scl))     # generate k vectors
yy=Y+n       


# shadow plot
plt.plot(t,yy)
plt.xlabel(r'$t$',size=20)
plt.ylabel(r'$f(t)+n$',size=20)
plt.title(r'Plot of the data to be fitted')
plt.grid(True)
savetxt("fitting.dat",c_[t,yy])
plt.show()

'''
ideal_a = array([1.05 for i in range(k)])
ideal_b = array([-0.105 for i in range(k)])
error_matrix_a = mse(a_est,ideal_b,real)  
error_matrix_b = mse(ideal_a,b_est,real)  #passing real function without noise
a_error = error_matrix_a.diagonal()
b_error = error_matrix_b.diagonal()
'''