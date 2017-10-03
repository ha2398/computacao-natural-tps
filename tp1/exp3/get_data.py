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

plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

vh1 = [0] * 50
vh2 = [0] * 50

h1 = open('house-p50-g50-c06-m03-e2-s0.txt', 'r')
h2 = open('house-p50-g50-c09-m005-e2-s1.txt', 'r')

data = open('values.dat', 'w')
i = 0
for line in h1:
	if "Best fitness:" in line:
		v = float(line.split()[2])
		vh1[i] += v
		i += 1

i = 0
for line in h2:
	if "Best fitness:" in line:
		v = float(line.split()[2])
		vh2[i] += v
		i += 1


h1.close()
h2.close()

for i in range(50):
	data.write(str(i+1) + '\t' + str(vh1[i]) + '\t' + str(vh2[i]) + '\n')

data.close()
plot_cmds.write('plot \'values.dat\' u 12 title \'C=0.6, M=0.3\' smooth bezier, \\\n\'values.dat\' u 13 title \'C=0.9, M=0.05\' smooth bezier')
plot_cmds.close()

sp.call(['gnuplot', 'plot_commands.gp'])