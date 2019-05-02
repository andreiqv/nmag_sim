# case whet axis-3 and 2 perpend to cylinder axis and axis-1 is parallel to it.

import math
from math import sin, cos, pi
import numpy as np
from numpy.linalg import inv

c11 = 307.1 # GPa
c12 = 165.0
c13 = 102.7
c33 = 358.1

s11 = 4.73*0.001  # GPa^-1
s12 = -2.31*0.001
s44 = 13.2*0.001

lmA = -50e-6
lmB = -107e-6 

Kef = 2.52e5
Kd = -3.8e5
Kmc = 2.2e5
Kme = Kef - Kd - Kmc
print('Kme = ' + str(Kme/1e5))

print(1/(s11+s12))
k = c11 + c12 - 2.0*c13**2/c33
k0 = k*1e9
print('k='+str(k))

lm0 = lmA + lmB
print('lm0=' + str(lm0*1e6) + ' *e-6')
eps = Kme/(-1*k0*lm0)
print('eps = ' + str(eps))

tau = -Kme/lm0
print('tau = ' + str(tau/1e9))

#------------
print('----\n case 2\n------')

a = c11
b = c12
c = c13
d = c33

B1 = -8.1
B2 = -29
B3 = 28.2

kzn = (a - b) * (a*d + b*d - 2*c*c)
k1 = (a*d + b*c - a*c - c*c) / kzn
k2 = (-a*c + b*c - b*d + c*c) / kzn
k3 = (a*a - b*b + b*c - a*c) / kzn

print('k1 = ' + str(k1))
print('k2 = ' + str(k2))
print('k3 = ' + str(k3))

print('\na) approx with B1=0')

b1 = B1*k1
b2 = B2*k3
b3 = B3*(k1+k2)
K0 = ( b2 + b3 ) * 1e6

print('b1 = ' + str(b1))
print('b2 = ' + str(b2))
print('b3 = ' + str(b3))

print('K0 = b2 + b3 = ' + str(K0/1.0e6))
print('Kme = ' + str(Kme))
print('tau = ' + str(Kme/K0))

print('---------')
print('b) calc B1')
K01 = -3.0/4.0*b1+b2+b3
K02 = b1+b2+b3
print('K01 = ' + str(K01))
print('K02 = ' + str(K02))
print(0.412/K01)
print(0.412/K02)

#-----------------------

print('\nb) common case')
th = 0.0*pi/180.0
print('th=' + str(th))

print('\nSolve with matrix:')
A = np.matrix([[a,b,c],[b,a,c],[c,c,d]])
print('A = ' + str(A))
B = inv(A)
T = np.matrix([[sin(th)],[cos(th)],[1]])
print('T = ' + str(T))
X=B*T
print('X = ' + str(X))

k1, k2, k3 = X[0,0], X[1,0], X[2,0]
print('k1 = ' +str(k1))
print('k2 = ' +str(k2))
print('k3 = ' +str(k3))
print('k2/k1 = ' + str(k2/k1))

b1 = B1*k1
b2 = B2*k3
b3 = B3*(k1+k2)
print('b1 = ' + str(b1))
print('b2 = ' + str(b2))
print('b3 = ' + str(b3))

K01 = k2/k1*b1+b2+b3
K02 = b1+b2+b3
print('K01 = ' + str(K01))
print('K02 = ' + str(K02))
print(0.412/K01)
print(0.412/K02)

#--------------------------

if False:
	l = []
	for i1 in range(1,10):
		x1 = 0.1*i1
		for i2 in range(1,10):
			x2 = 0.1*i2
			g = (x1**2 - 3.0/4.0*x2**2) / (x1**2 + x2**2)
			l += [g]
			#print('({0:1.1},{1:1.1}): g={2:2.2}'.format(x1,x2,g))
	print(max(l))
	print(min(l))