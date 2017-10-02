#!/usr/bin/env python3

import os
import subprocess as sp

X = 'Geração'
Y = 'Melhor Fitness'
TITLE = X + ' x ' + Y

try:
    os.remove('plot_commands.gp')
    os.remove('graph.png')
    os.remove('values.dat')
except OSError:
    pass

files = [f for f in os.listdir('./') if os.path.isfile(f) and f != 'get_data.py']
print(files)

plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

values = [0] * 50

data = open('values.dat', 'w')
for file in files:
	cur_file = open(file, 'r')

	counter = 0
	for line in cur_file:
		if "Best fitness:" in line:
			v = float(line.split()[2])
			values[counter] += v
			counter += 1

	cur_file.close()


for i in range(len(values)):
	values[i] = values[i] / len(files)
	data.write(str(i+1) + '\t' + str(values[i]) + '\n')

data.close()
plot_cmds.write('plot \'values.dat\' u 1:2 notitle smooth bezier')
plot_cmds.close()

sp.call(['gnuplot', 'plot_commands.gp'])