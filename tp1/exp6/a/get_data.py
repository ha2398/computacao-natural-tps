#!/usr/bin/env python3

import os
import subprocess as sp

X = 'Geração'
Y = 'Indivíduos Repetidos'
TITLE = X + ' x ' + Y

try:
    os.remove('plot_commands.gp')
    os.remove('graph.png')
    os.remove('values.dat')
except OSError:
    pass

plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

vh1 = [0] * 50

h1 = open('k7g50p500c09m005e2k7s0.txt', 'r')

data = open('values.dat', 'w')
i = 0
for line in h1:
	if "Number of repeated individuals:" in line:
		v = float(line.split()[4])
		vh1[i] += v
		i += 1

h1.close()

for i in range(50):
	data.write(str(i+1) + '\t' + str(vh1[i]) + '\n')

data.close()
plot_cmds.write('plot \'values.dat\' u 1:2 notitle smooth bezier')
plot_cmds.close()

sp.call(['gnuplot', 'plot_commands.gp'])