#!/usr/bin/env python3

import os
import subprocess as sp

X = 'Iteração'
Y = 'Custo da Melhor Solução'
TITLE = 'SJC2.dat: ' + X + ' x ' + Y

it = 25

try:
	sp.call(['rm', '-rf', 'plot_commands.gp'])
	sp.call(['rm', '-rf', 'graph.png'])
	sp.call(['rm', '-rf', '*.dat*'])
except OSError:
    pass

files = sorted([f for f in os.listdir('./') if f != 'plot.py' and 'dat' not in f])

plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

for file in files:
	values = [0] * it
	counter = 0
	cur_file = open(file, 'r')
	for line in cur_file:
		if 'Best global' in line:
			values[counter] += float(line.split()[2])
			counter += 1

	cur_file.close()
	best_dat = open(file[0:3] + '.dat', 'w')
	for i in range(len(values)):
		best_dat.write(str(i+1) + '\t' + str(values[i]) + '\n')
	best_dat.close()

plot_cmds.write('plot ')

for i in range(len(files)):
	plot_cmds.write('\''+ files[i][0:3] + '.dat\' u 1:2 title \'' + files[i][0:3] + '\' smooth bezier')

	if i < len(files) - 1:
		plot_cmds.write(', ')

plot_cmds.close()
sp.call(['gnuplot', 'plot_commands.gp'])