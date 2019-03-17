#rm *.vtk; ./nsim/bin/nsim sphere_Co1.py --clean; 

import os

os.system('rm *.vtk')

# write without ".py"

#ls = ['cyl_15_100_af']
#ls = ['cyl_20_100_af']
ls = ['cyl_cofe']


for x in ls:
	cmd0 = '/home/z/nano/nmag-0.2.1/nsim/bin/nsim {0}.py --clean'.format(x);
	cmd1 = '/home/z/nano/nmag-0.2.1/nsim/bin/nmagpp --dump {0} 1>/dev/null'.format(x); 
	cmd2 = '/home/z/nano/nmag-0.2.1/nsim/bin/nmagpp --vtk {0}.vtk {0}'.format(x)
	
	print('cmd: ' + cmd0)
	os.system(cmd0)
	
	ch = input('Enter q for exit or other for continue: ')
	if ch != 'q':
		print('cmd: ' + cmd1)
		os.system(cmd1)
		print('cmd: ' + cmd2)	
		os.system(cmd2)
