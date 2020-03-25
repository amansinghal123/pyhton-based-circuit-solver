import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import *


n = 51              #number of coeff required
axis = range(51)    #discrete x axis
nn = (n-1)//2       # number of a and b coeff
N = 400
x = np.linspace(0,2*np.pi,N+1)
x = x[:-1]


#1    
def exp(x):
    exp.name = "exp(x)"
    return np.exp(x)
def coscos(x):
    coscos.name = "coscos(x)"
    return np.cos(np.cos(x))

m = np.linspace(-2*np.pi, 4*np.pi, 201)
plt.loglog(m, exp(m), basey=10)
plt.xlabel(r"$x$",size=15)
plt.ylabel(r"$exp(x)$",size=15)
plt.title(r"Plot of the exp(x)")
plt.show()
plt.plot(m,coscos(m))
plt.xlabel(r"$x$",size=15)
plt.ylabel(r"$coscos(x)$",size=15)
plt.title(r"Plot of the coscos(x)")
plt.show()


#2
def coeff_a(f,n):
    def a_integrand(x,f,n):
        return f(x)*np.cos(n*x)
    a = [quad(a_integrand, 0, 2*np.pi, args=(f,0))[0]/(2*np.pi)]
    for i in range(1,n+1):
        a.append(quad(a_integrand, 0, 2*np.pi, args=(f,i))[0]/(np.pi))
    return a
    
def coeff_b(f,n):
    def b_integrand(x,f,n):
        return f(x)*np.sin(n*x)
    b = []
    for i in range(1,n+1):
        b.append(quad(b_integrand,0,2*np.pi,args=(f,i))[0]/(np.pi))
    return b
    
'''
print(coeff_a(exp,n))
print(coeff_b(exp,n))
print()
print(coeff_a(coscos,n))
print(coeff_b(coscos,n))
'''

#3
def coeff_vector(f):
    l = [coeff_a(f,nn)[0]]
    abs_l = [np.absolute(coeff_a(f,nn)[0])]
    for i in range(nn):
        abs_l.append(np.absolute(coeff_a(f,nn)[i+1]))
        l.append(coeff_a(f,nn)[i+1])
        abs_l.append(np.absolute(coeff_b(f,nn)[i]))
        l.append(coeff_b(f,nn)[i])
    v = np.c_[l]
    abs_v = np.c_[abs_l]
    plt.loglog(axis,abs_v,'ro',label="loglog plot of coeff of {}".format(f.name))
    plt.xlabel(r"$x$",size=15)
    plt.ylabel(r"${}$".format(f.name),size=15)
    plt.title(r"Plot of the data from integration")
    plt.legend()
    plt.show()
    plt.semilogy(axis,abs_v,'ro',label="semilog plot of coeff {}".format(f.name))
    plt.xlabel(r'$x$',size=15)
    plt.ylabel(r"${}$".format(f.name),size=15)
    plt.title(r'Plot of the data from integration')
    plt.legend()
    plt.show()
    return v
    
v1 = coeff_vector(exp)
v2 = coeff_vector(coscos)


#4 and #5
def lst_coeff(f): 
    b = []
    for i in x:
        b.append(f(i))
    A = np.zeros((N,51)) 
    A[:,0] = 1 
    for k in range(1,nn+1):
        A[:,2*k-1] = np.cos(k*x) 
        A[:,2*k] = np.sin(k*x)
    c = np.linalg.lstsq(A,b)[0]
    plt.loglog(axis,np.absolute(c),'go',label="loglog plot of coeff of {}".format(f.name))
    plt.xlabel(r"$x$",size=15)
    plt.ylabel(r"${}$".format(f.name),size=15)
    plt.title(r"Plot of the data from least square approximation")
    plt.legend()
    plt.show()
    plt.semilogy(axis,np.absolute(c),'go',label="semilog plot of coeff {}".format(f.name))
    plt.xlabel(r'$x$',size=15)
    plt.ylabel(r"${}$".format(f.name),size=15)
    plt.title(r'Plot of the data from least square approximation')
    plt.legend()
    plt.show()
    a = np.c_[c]
    return a,A
    
c1 = lst_coeff(exp)[0]
c2 = lst_coeff(coscos)[0]


#6
error_1 = np.absolute(v1-c1)
error_2 = np.absolute(v2-c2)
print("error1",error_1)
print("error2",error_2)
print(sorted(np.ndarray.tolist(error_1))[-1])
print(sorted(np.ndarray.tolist(error_2))[-1])


#7
plt.plot(x,np.dot(lst_coeff(exp)[1],c1),"go",markersize=2.5,label="estimated function from fourier coefficients")
plt.plot(x,exp(x),label="actual function exp(x)")
plt.xlabel(r"$x$",size=15)
plt.ylabel(r"$exp(x)$",size=15)
plt.title(r"Plot of the actual and estimated function")
plt.legend()
plt.show()
plt.plot(x,np.dot(lst_coeff(coscos)[1],c2),"go",markersize=2.5,label="estimated function from fourier coefficients")
plt.plot(x,coscos(x),label="actual function coscos(x)")
plt.xlabel(r"$x$",size=15)
plt.ylabel(r"$coscos(x)$",size=15)
plt.title(r"Plot of the actual and estimated function")
plt.legend()
plt.show()

#################################################################################################################################