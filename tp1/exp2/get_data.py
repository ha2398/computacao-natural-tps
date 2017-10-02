#!/usr/bin/env python3

import os
import subprocess as sp

X = 'População Inicial'
Y = 'Melhor Fitness'
TITLE = X + ' x ' + Y

try:
    os.remove('plot_commands.gp')
    os.remove('graph.png')
    os.remove('values.dat')
except OSError:
    pass

files = [f.replace('.out', '') for f in os.listdir('./') if os.path.isfile(f) and f != 'get_data.py']

print(files)

plot_cmds = open('plot_commands.gp', 'w')

plot_cmds.write('clear\nreset\nunset key\n')


plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

plot_cmds.write('set style data histogram\n')
plot_cmds.write('set style fill solid border\n')
plot_cmds.write('set style histogram clustered\n')

files.sort()

data = open('values.dat', 'w')
for file in files:
	cur_file = open(str(file) + '.out', 'r')

	data.write(str(file) + '\t')

	counter = 0
	for line in cur_file:
		if "Best fitness:" in line:
			v = float(line.split()[2])
			counter += 1

			if (counter % 10) == 0:
				data.write(str(v) + '\t')

	cur_file.close()
	data.write('\n')

data.close()

plot_cmds.write('plot for [COL=2:6] \'values.dat\' using COL:xticlabels(1) title columnheader')
plot_cmds.close()
sp.call(['gnuplot', 'plot_commands.gp'])