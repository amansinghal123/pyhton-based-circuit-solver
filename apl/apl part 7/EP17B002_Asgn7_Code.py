from sympy import symbols, lambdify, Matrix, numer, denom
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp

ww = np.logspace(-1, 10, 1000)
ss = 1j*ww
s = symbols('s')

def lowpass(R1,R2,C1,C2,G,Vi):
    A=Matrix([[0,0,1,-1/G],
              [-1/(1+s*R2*C2),1,0,0],
              [0,-G,G,1],
              [-1/R1-1/R2-s*C1,1/R2,0,s*C1]])
    b=Matrix([0,0,0,Vi/R1])
    V=A.inv()*b
    return (A,b,V)
    
def highpass(R1,R2,C1,C2,G,Vi):
    s = symbols('s')
    A = Matrix([[0,0,1,-1/G],
                [-s*R2*C2/(1+s*R2*C2),1,0,0],
                [0,-G,G,1],
                [-1/R1-s*C2-s*C1,s*C2,0,1/R1]])
    b = Matrix([0,0,0,-Vi*s*C1])
    V = A.inv()*b
    return (A,b,V)

def inp(f1,f2,t):
    return (np.sin(2*np.pi*f1*t) * np.cos(2*np.pi*f2*t))*np.heaviside(t,2)

def damped_sinusoid(f,a,t):
    return np.cos(2*np.pi*f*t)* np.exp(-a*t)*np.heaviside(t,2)


#pdf
A_lp,b_lp,V_lp=lowpass(10000,10000,1e-9,1e-9,1.586,1)
Vo_lp = V_lp[3]
hf_lp = lambdify(s,Vo_lp,'numpy')
bode_output_lp = hf_lp(ss)
plt.loglog(ww,abs(bode_output_lp),lw=2)
plt.title("bode plot of lowpass filter")
plt.xlabel('frequency')
plt.ylabel('H(jw)')
plt.grid(True)
plt.show()

numerator_lp = [float(numer(Vo_lp.simplify()).coeff(s, 2)),float(numer(Vo_lp.simplify()).coeff(s, 1)),float(numer(Vo_lp.simplify()).coeff(s, 0))]
denominator_lp = [float(denom(Vo_lp.simplify()).coeff(s, 2)), float(denom(Vo_lp.simplify()).coeff(s, 1)), float(denom(Vo_lp.simplify()).coeff(s, 0))]


#1
v, t = sp.step([numerator_lp, denominator_lp], None, np.arange(0, 1e-3, 1e-6))
plt.plot(v, t)
plt.title("Step response of lowpass filter")
plt.grid(True)
plt.xlabel('t')
plt.ylabel('Vo')
plt.show()


#2
t1 = np.arange(0,1e-2,1e-6)
x,y,svec = sp.lsim([numerator_lp, denominator_lp], inp(1e3,1e6,t1), t1)
plt.plot(x, y)
plt.grid(True)
plt.title("response of low pass filter for sin(2e3*pi*t)+cos(2e6*pi*t) as input")
plt.xlabel('t')
plt.ylabel('Vo')
plt.show()


#3
A_hp,b_hp,V_hp=highpass(10000,10000,1e-9,1e-9,1.586,1)
Vo_hp = V_hp[3]
hf_hp = lambdify(s,Vo_hp,'numpy')
bode_output_hp = hf_hp(ss)
plt.loglog(ww,abs(bode_output_hp),lw=2)
plt.title("bpde plot of highpass filter")
plt.xlabel('frequency')
plt.ylabel('H(jw)')
plt.grid(True)
plt.show()

numerator_hp = [float(numer(Vo_hp.simplify()).coeff(s, 2)),float(numer(Vo_hp.simplify()).coeff(s, 1)),float(numer(Vo_hp.simplify()).coeff(s, 0))]
denominator_hp = [float(denom(Vo_hp.simplify()).coeff(s, 2)), float(denom(Vo_hp.simplify()).coeff(s, 1)), float(denom(Vo_hp.simplify()).coeff(s, 0))]


#4a(low frequency)
t2 = np.arange(1e-5, 5e-4, 1e-7)
x,y,svec = sp.lsim([numerator_hp, denominator_hp], damped_sinusoid(1e4,1e6,t2), t2)
plt.plot(x, y)
plt.grid(True)
plt.title("response of high pass filter for cos(2e4*pi*t)*exp(-1e6*t) as input")
plt.xlabel('t')
plt.ylabel('Vo')
plt.show()


#4b(high frequency)
t2 = np.arange(1e-9, 5e-7, 1e-9)
x,y,svec = sp.lsim([numerator_hp, denominator_hp], damped_sinusoid(1e7,1e6,t2), t2)
plt.plot(x, y)
plt.grid(True)
plt.title("response of high pass filter for cos(2e7*pi*t)*exp(-1e6*t) as input")
plt.xlabel('t')
plt.ylabel('Vo')
plt.show()



#5
A_hp,b_hp,V_hp=highpass(10000,10000,1e-9,1e-9,1.586,1/s)
Vo_hp = V_hp[3]
hf_hp = lambdify(s,Vo_hp,'numpy')
bode_output_hp = hf_hp(ss)
plt.loglog(ww,abs(bode_output_hp),lw=2)
plt.title("replacing Vi from 1 to 1/s for high pass filter")
plt.xlabel('frequency')
plt.ylabel('H(jw)')
plt.grid(True)
plt.show()
