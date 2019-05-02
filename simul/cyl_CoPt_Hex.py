# http://hostelsminsk.by/ad-category/hotels/

#nmesh = 'z_cylinder_D15_H100_h15.nmesh.h5'
nmesh = 'z_cylinder_D20_H100_h2.nmesh.h5'

#--------------------------

import nmag
from nmag import SI, every, at
import math
from math import sqrt

READFILE = False

#create simulation object
sim = nmag.Simulation()

# Function to compute the scalar product of the vectors a and b
def scalar_product(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
sc = scalar_product


# for pure Co
#Ms0 = 1400e3   # A/m
#A_ex = 1.54e-11	# J/m
#kmc = 2.37*1e5

# CoPt(5%)
Ms0 = 1330e3   # A/m
A_ex = 1.46e-11	# J/m
kmc = 2.0e5 # J/m3

tau = -3.0  # in GPa
#tau=-10.0  # in GPa
#tau=-15.0  # in GPa
#tau=-18.0  # in GPa

#kme = 5.35*1e5   # 5.35*1e5
#k1 = kmc + kme 	# J/m^3
start_magn_dir = [1,1,1]


hex_axis = 'Z'  # direction of the hexagonal axis
print('hex_axis = ' + hex_axis)

fw = open('_out.txt', 'a')
fw.write('hex_axis = {0}, tau={1}, nmesh={2};\n'.format(hex_axis, tau, nmesh))
fw.close()

# define magnetic material
# define magnetic material Cobalt (data from OOMMF materials file)

# uniaxial anisotropy
#Co = nmag.MagMaterial(name="Co", Ms=SI(Ms0, "A/m"),exchange_coupling=SI(A_ex, "J/m"),
#          anisotropy=nmag.uniaxial_anisotropy(axis=crist_anisotropy, K1=SI(k1, "J/m^3")))


# **CUBIC** anisotropy
#Co = nmag.MagMaterial(name="Co", Ms=SI(Ms0, "A/m"), exchange_coupling=SI(A_ex, "J/m"),
#	anisotropy=nmag.cubic_anisotropy(axis1=[1, 0, 0], axis2=[0, 1, 0], K1=SI(k1, "J/m^3")))


# MY own uniaxial anisotropy

K1=SI(kmc, "J/m^3")
#K2=SI(2.00*1e5, "J/m^3")

ex = [1, 0, 0]  # = norm_axis
ey = [0, 1, 0]
ez = [0, 0, 1]

B1 = SI(-8.1 * 1e6, "J/m^3") 	
B2 = SI( -29 * 1e6, "J/m^3")	
B3 = SI(28.2 * 1e6, "J/m^3") 	

if hex_axis == 'X':
	(n1, n2, n3) = (ey, ez, ex)  # hex. axis [0001] || x
	eps1 = 0.00403  * tau
	eps2 = -0.00300 * tau
	eps3 = 0.00249  * tau

if hex_axis == 'Z':
	(n1, n2, n3) = (ex, ey, ez)  # hex. axis [0001] || z
	eps1 = 0.00242  * tau
	eps2 = 0.00242  * tau
	eps3 = -0.00139 * tau	

def my_anisotropy(m):
	#a = scalar_product(norm_axis, m)
	#return -K1*a**2 - K2*a**4
	#return K1*( sc(ey,m)**2 + sc(ez,m)**2 )  # equals to return -K1*a**2
	a1 = sc(m, n1)
	a2 = sc(m, n2)
	a3 = sc(m, n3)
	return K1*( a1**2 + a2**2 ) + B1*(a1**2 * eps1 + a2**2 * eps2) + (a1**2 + a2**2) * (B2 * eps3 + B3 * (eps1 + eps2))
 

Co = nmag.MagMaterial(name="Co", Ms=SI(Ms0, "A/m"), exchange_coupling=SI(A_ex, "J/m"),
          anisotropy=my_anisotropy, anisotropy_order=2)


# load mesh
sim.load_mesh(nmesh,
              [('cylinder', Co)],
              unit_length = SI(1e-9, 'm'))

# set initial magnetisation
#sim.set_m([1,0,0])
sim.set_m( start_magn_dir)

# set external field
#sim.set_H_ext([0,0,0], SI('A/m'))

# Save and display data in a variety of ways
#sim.save_data(fields='all') # save all fields spatially resolved
                            # together with average data

# sample demag field through sphere
#for i in range(-10,11):
    #x = i*1e-9                      #position in metres
    #H_demag = sim.probe_subfield_siv('H_demag', [x,0,0])
    #print "x =", x, ": H_demag = ", H_demag
    
#sim.set_m([0.999847695156, 0, 0.01745240643731])    
ns = SI(1e-9, "s") # corresponds to one nanosecond

#sim.relax(save = [('averages', every('time', 0.01*ns)), ('fields', every('time', 0.05*ns) | at('convergence'))])
sim.relax(save = [('fields', at('step', 0) | at('stage_end'))])



#------------  magn to file

outfile = '_out_' + nmesh.split('.')[0] + '.txt'
outf = open(outfile, 'w')
outf.write('outfile\n')
outf.write(nmesh + '\n')
outf.write('tau = {0} \n'.format(tau))



for i in range(-50, 55, 5):
	x = 0                      #position in metres
	y = 0
	z = i*1e-9
	m = sim.probe_subfield_siv('m_Co', [x, y, z])
	#print('m = ' + str(m))

	if m is not None:
		val = sqrt(m[0]**2 + m[1]**2 + m[2]**2)
		#s = "x = {0:4}:  m = {1:2.2}  =  [{2:2.2}, {3:2.2}, {4:2.2}]".format(x, val, round(m[0],2), round(m[1],2), round(m[2],2))
		s = "i = {0:4}:  mx = {1:2.3}, mz = {2:2.3}".format(i , round(m[0], 2), round(m[2], 2))
	else:
		s = 'i = None'

	print(s)
	outf.write(s + '\n')
		
outf.close()

print('END')


import os
d = 0.2
for i in range(0,5):
	f = 1200 if i%2 == 0 else 1500	
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (d, f))

print('---------------------')
print('tau = {}'.format(tau))	