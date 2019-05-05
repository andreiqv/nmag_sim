# http://hostelsminsk.by/ad-category/hotels/

#nmesh = 'z_cylinder_D10_H100_h15.nmesh.h5'
#nmesh = 'z_cylinder_D10_H20_h1.nmesh.h5'
#nmesh = 'z_cylinder_D20_H20_h15.nmesh.h5'
nmesh = 'z_cylinder_D20_H100_h2.nmesh.h5'

#nmesh = 'z_cylinder_D20_H200_h3.nmesh.h5'
#nmesh = 'z_cylinder_D20_H400_h3.nmesh.h5'

#--------------------------

import nmag
from nmag import SI, every, at
import math
from math import sqrt
import sys

READFILE = False

#create simulation object
sim = nmag.Simulation()

# Function to compute the scalar product of the vectors a and b
def scalar_product(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
sc = scalar_product

Ms0 = 400e3   # A/m
A_ex = 0.66e-11	# J/m
kmc = 0.45e5 # J/m^3 - MCA

# (-0.3 too long calc for D10_H20)

tau = 5.0  # in GPa 
#tau=-3.0  # in GPa

start_magn_dir = [1, 1, 1]

fw = open('_out.txt', 'a')
fw.write('cubic: tau={0}, nmesh={1};\n'.format(tau, nmesh))
fw.close()

# define magnetic material
# MY own CUBIC anisotropy

K1 = SI(kmc, "J/m^3")
#K2=SI(2.00*1e5, "J/m^3")

ex = [1, 0, 0]  # = norm_axis
ey = [0, 1, 0]
ez = [0, 0, 1]

B1 = SI(-15.3 * 1e6, "J/m^3") 

(n1, n2, n3) = (ex, ey, ez) 
eps1 = 0.00276  * tau
eps2 = 0.00276  * tau
eps3 = -0.00311 * tau	

def my_anisotropy(m):
	#a = scalar_product(norm_axis, m)
	#return -K1*a**2 - K2*a**4
	#return K1*( sc(ey,m)**2 + sc(ez,m)**2 )  # equals to return -K1*a**2
	a1 = sc(m, n1)
	a2 = sc(m, n2)
	a3 = sc(m, n3)
	return K1*( a1**2 * a2**2 + a1**2 * a3**2 + a2**2 * a3**2 ) + B1*(a1**2 * eps1 + a2**2 * eps2 + a3**2 * eps3)
 
material_name = 'CoFe'
material = nmag.MagMaterial(name=material_name, 
		Ms=SI(Ms0, "A/m"), 
		exchange_coupling=SI(A_ex, "J/m"),
		anisotropy=my_anisotropy, anisotropy_order=4)

# load mesh
sim.load_mesh(nmesh,
              [('cylinder', material)],
              unit_length = SI(1e-9, 'm'))

# set initial magnetisation
#sim.set_m([1,0,0])
sim.set_m(start_magn_dir)

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


# print magnetization distribution:
for i in range(-100, 100, 10):
	x = 0                      #position in metres
	y = 0
	z = i*1e-9
	m = sim.probe_subfield_siv('m_{}'.format(material_name), [x, y, z])

	if m is not None:
		val = sqrt(m[0]**2 + m[1]**2 + m[2]**2)
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
	f = 1200 if i%2==0 else 1500	
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (d, f))


print('---------------------')
print('hex_axis = {}'.format(hex_axis))
print('tau = {}'.format(tau))	