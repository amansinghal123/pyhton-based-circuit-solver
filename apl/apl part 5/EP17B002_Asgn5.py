from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
from numpy import *
import matplotlib.pyplot as plt
import sys

Nx = 25 # size along x
Ny = 25 # size along y
r = 0.35  # radius of central lead
Niter = 1500 # number of iterations to perform
nx = (Nx - 1)//2
ny = (Ny - 1)//2

print("pass values of sizex, sizey, radius and number of iterations")
x = sys.argv
if(len(x) != 5):                                     
    print('invalid input')
    sys.exit()
else:
    Nx = int(x[1]) # size along x
    Ny = int(x[2]) # size along y
    r = float(x[3])  # radius of central lead
    Niter = int(x[4]) # number of iterations to perform
    nx = (Nx - 1)//2
    ny = (Ny - 1)//2
    
    #initialising phi
    phi = zeros((Nx,Ny))
    x = linspace(-0.5,0.5,Nx)
    y = linspace(-0.5,0.5,Ny)
    Y,X = meshgrid(y,x)
    ij = where(X*X + Y*Y <= r*r)
    phi[ij] = 1
    
    #plotting initial phi
    plt.contourf(X,Y,phi)
    plt.xlabel(r'x',size=15)
    plt.ylabel(r'y',size=15)
    plt.title(r'Contour plot of voltage initially')
    plt.legend()
    plt.show()
    
    #iterations
    errors = zeros(Niter)
    zero_row = zeros((1,Nx-2))
    for k in range(Niter):
        oldphi = phi.copy()

        phi[1:-1,1:-1]=0.25*(phi[1:-1,0:-2] + phi[1:-1,2:] + phi[0:-2,1:-1] + phi[2:,1:-1]) 
        #averaging the potential
    
        #boundary conditions
        phi[1:-1,0] = phi[1:-1,1]    # left col
        phi[1:-1,-1] = phi[1:-1,-2]  # right col
        phi[-1,1:-1] = phi[-2,1:-1]    # top row

        #corners boundary condition
        phi[-1,-1] = phi[-1,-2]
        phi[-1,0] = phi[-1,1]
        
        #maintaining 1V in the middle
        phi[ij] = 1
      
        #error
        errors[k]=(abs(phi-oldphi)).max()

    #plotting error
    ax = range(0,Niter,Niter//30)
    axis = range(Niter//3,Niter+1,Niter//30)
    plt.semilogy(ax,errors[0:Niter:Niter//30],'ro',label="semilog plot of error")
    #plt.loglog(axis,errors[(Niter//3)-1:Niter:Niter//30],'bo',label="semilog plot of error")
    plt.xlabel(r'$x$',size=15)
    plt.ylabel(r"$error",size=15)
    plt.title(r'Plot of error')
    plt.legend()
    plt.show()
    
    #plotting 3d voltage
    fig1 = plt.figure(4) # open a new figure
    ax = p3.Axes3D(fig1) # Axes3D is the means to do a surface plot
    plt.title('The 3-D surface plot of the potential')
    surf = ax.plot_surface(Y, X, phi, rstride=1, cstride=1, cmap=plt.cm.jet)
    plt.show()

    #plotting contour voltage plot
    plt.contour(Y,X,phi)
    plt.plot(Y[ij],X[ij],"ro")
    plt.title(r'Contour plot of voltage')
    plt.xlabel(r'$x$',size=15)
    plt.ylabel(r'$y$',size=15)
    plt.legend()
    plt.show()

    #jx and jy matrices from differetiation
    jx = zeros((Ny,Nx))
    jy = zeros((Ny,Nx)) 
    jx[1:-1,1:-1] = 0.5*(phi[1:-1,0:-2] - phi[1:-1,2:])
    jy[1:-1,1:-1] = 0.5*(phi[:-2,1:-1] - phi[2:,1:-1])
    
    #zeroing tangential components
    jx[0,0:] = 0
    jx[-1,0:] = 0
    jx[0:,0] = 0
    jx[0:,-1] = 0
    
    #zeroing perpendicular components
    jy[0,0:] = 0
    jy[-1,0:] = 0
    jy[0:,0] = 0
    jy[0:,-1] = 0
    
    #plotting current
    plt.quiver(x,y,jx,jy)
    plt.plot(Y[ij],X[ij],"ro")
    plt.title(r'plot of current flow')
    plt.xlabel(r'x',size=15)
    plt.ylabel(r'y',size=15)
    plt.legend()
    plt.show()

    # finding temeperature similar to finding potential
    T = zeros((Nx,Ny))
    T[ij] = 300
    for k in range(Niter):

        T[1:-1,1:-1]=0.25*(T[1:-1,0:-2] + T[1:-1,2:] + T[0:-2,1:-1] + T[2:,1:-1] - jx[1:-1,1:-1]**2 -jy[1:-1,1:-1]**2)

        T[1:-1,0] = T[1:-1,1]       # left col
        T[1:-1,-1] = T[1:-1,-2]     # right col
        T[-1,1:-1] = T[-2,1:-1]     # top row

        T[-1,-1] = T[-1,-2]         #corners
        T[-1,0] = T[-1,1]           #corners
        T[-1,1:-1] = 300 
        T[ij] = 300
        
    plt.contour(Y,X,T)
    plt.plot(Y[ij],X[ij],"ro")
    plt.xlabel(r'x',size=15)
    plt.ylabel(r'y',size=15)
    plt.title(r'Contour plot of temperature')
    plt.legend()
    plt.show()
    
    fig2 = plt.figure(4) # open a new figure
    ax = p3.Axes3D(fig2) # Axes3D is the means to do a surface plot
    plt.title('The 3-D surface plot of the temperature')
    surf = ax.plot_surface(Y, X, T, rstride=1, cstride=1, cmap=plt.cm.jet)
    plt.show()
