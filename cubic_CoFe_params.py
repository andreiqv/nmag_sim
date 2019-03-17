import numpy as np
from numpy.linalg import inv


def find_eps(c11, c12):
	print('Solve with matrix:')
	A = np.matrix([[c11, c12, c12], [c12, c11, c12], [c12, c12, c11]])
	B = inv(A)
	T = np.matrix([[1],[1],[0]])
	X = B*T
	print(X)

print('In Pa:')
find_eps(c11=225.6e9, c12=142.16e9)

print('\nIn GPa:')
find_eps(c11=225.6, c12=142.16)

c11 = 225.6e9
c12 = 142.16e9
lm100 = 197e-6 / 3 * 2;
B1 = - 3/2 * lm100 * (c11 - c12)
print('B1 = {0} = {0:.2e}'.format(B1))




"""
B1 = -9.2  # GPa

s11 = 8.81*0.001  # GPa^-1
s12 = -3.51*0.001

#lmA = -50e-6
#lmB = -107e-6 

Kme = 5.35e5

print('Kme = ' + str(Kme/1e5) + ' *10^5')


print('----\n cubic \n------')

lam = -50*1e-6;
sig = - 2.0/3.0 * Kme / lam
print('sig = ' + str(sig / 1e9) + ' GPa')

"""

