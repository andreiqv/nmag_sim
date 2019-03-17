
#--------------------------

import nmag
from nmag import SI, every, at
import math
from math import sqrt

#create simulation object
sim = nmag.Simulation()

Ms0 = 1400e3   # A/m
A_ex = 30e-12	# J/m
k1 = 6.32e5 	# J/m^3

f = open('_angle.txt')
angle = float(f.readline().split(';')[0])
print('angle = ' + str(angle))

if int(angle)==90:
	crist_anisotropy = [0, 0, 1]
else:
	crist_anisotropy = [1, 0, math.tan(angle/180.0*math.pi)]

print(crist_anisotropy)
f.close()

fw = open('_out.txt', 'a')
fw.write('angle = {0}, an={1}, nmesh={2};\n'.format(angle, crist_anisotropy, nmesh))
fw.close()

# define magnetic material
# define magnetic material Cobalt (data from OOMMF materials file)
Co = nmag.MagMaterial(name="Co",
                      Ms=SI(Ms0, "A/m"),
                      exchange_coupling=SI(A_ex, "J/m"),
                      anisotropy=nmag.uniaxial_anisotropy(axis=crist_anisotropy, K1=SI(k1, "J/m^3")))

# load mesh
sim.load_mesh(nmesh,
              [('cylinder', Co)],
              unit_length = SI(1e-9, 'm'))

# set initial magnetisation
sim.set_m([1,0,0])

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


outfile = '_out_' + nmesh.split('.')[0] + '.txt'
outf = open(outfile, 'w')
outf.write('Hello\n')

for i in range(-75,75,5):
	x = i*1e-9                      #position in metres
	y = 0
	z = 0
	m = sim.probe_subfield_siv('m', [x, y, z])

	if m is not None:
		val = sqrt(m[0]**2 + m[1]**2 + m[2]**2)
		s = "x = {0:4}:  m = {1:2.2}  =  [{2:2.2}, {3:2.2}, {4:2.2}]".format(x, val, round(m[0],2), round(m[1],2), round(m[2],2))
	else:
		s = 'x = None'

	print(s)
	outf.write(s + '\n')
		
outf.close()

print('END')
