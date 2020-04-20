from numpy import *
from matplotlib.pyplot import *
from pylab import *

# 1
x=random.rand(100)
X=fft.fft(x)
y=fft.ifft(X)
c_[x,y]
print(abs(x-y).max())

# 2
x=linspace(0,2*pi,128)
y=sin(5*x)
Y=fft.fft(y)
figure()
subplot(2,1,1)
plot(abs(Y),lw=2)
grid(True)
subplot(2,1,2)
plot(unwrap(angle(Y)),lw=2)
grid(True)
show()


# 3
x=linspace(0,2*pi,128)
y=sin(5*x)
Y=fft.fft(y)
figure()
subplot(2,1,1)
plot(abs(Y),lw=2)
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $\sin(5t)$")
grid(True)
subplot(2,1,2)
plot(unwrap(angle(Y)),lw=2)
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$k$",size=16)
grid(True)
savefig("fig9-1.png")
show()

# 4
x=linspace(0,2*pi,129);x=x[:-1]
y=sin(5*x)
Y=fft.fftshift(fft.fft(y))/128.0
w=linspace(-64,63,128)
figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-10,10])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $\sin(5t)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
ii=where(abs(Y)>1e-3)
plot(w[ii],angle(Y[ii]),'go',lw=2)
xlim([-10,10])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$k$",size=16)
grid(True)
savefig("fig9-2.png")
show()

# 5
t=linspace(0,2*pi,129);t=t[:-1]
y=(1+0.1*cos(t))*cos(10*t)
Y=fft.fftshift(fft.fft(y))/128.0
w=linspace(-64,63,128)
figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-15,15])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $\left(1+0.1\cos\left(t\right)\right)\cos\left(10t\right)$")
grid(True)

subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
savefig("fig9-3.png")
show()

# 6
t=linspace(-4*pi,4*pi,513);t=t[:-1]
y=(1+0.1*cos(t))*cos(10*t)
Y=fft.fftshift(fft.fft(y))/512.0
w=linspace(-64,64,513);w=w[:-1]

figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-15,15])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $\left(1+0.1\cos\left(t\right)\right)\cos\left(10t\right)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
savefig("fig9-4.png")
show()

# 7
t=linspace(-4*pi,4*pi,513);t=t[:-1]
y=sin(t)**3
Y=fft.fftshift(fft.fft(y))/512.0
w=linspace(-64,64,513);w=w[:-1]

figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-15,15])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $sin^3(t)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
savefig("fig9-4.png")
show()

# 8
t=linspace(-4*pi,4*pi,513);t=t[:-1]
y=cos(t)**3
Y=fft.fftshift(fft.fft(y))/512.0
w=linspace(-64,64,513);w=w[:-1]

figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-15,15])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $cos^3(t)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
savefig("fig9-4.png")
show()

# 9
t=linspace(-4*pi,4*pi,513);t=t[:-1]
y=cos(20*t + 5*cos(t))
Y=fft.fftshift(fft.fft(y))/512.0
w=linspace(-64,64,513);w=w[:-1]

figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-40,40])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $cos(20t + 5cos(t))$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
savefig("fig9-4.png")
show()


# 10
t=linspace(-4*pi,4*pi,513);t=t[:-1]
y=exp(-t**2/2)
Y=fft.fftshift(fft.fft(y))/512.0
w=linspace(-64,64,513);w=w[:-1]

figure()
subplot(2,1,1)
plot(w,abs(Y),lw=2)
xlim([-15,15])
ylabel(r"$|Y|$",size=16)
title(r"Spectrum of $exp(-t^2/2)$")
grid(True)
subplot(2,1,2)
plot(w,angle(Y),'ro',lw=2)
xlim([-15,15])
ylabel(r"Phase of $Y$",size=16)
xlabel(r"$\omega$",size=16)
grid(True)
savefig("fig9-4.png")
show()
