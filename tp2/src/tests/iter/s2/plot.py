#!/usr/bin/env python3

import os
import subprocess as sp

X = 'Iteração'
Y = 'Custo da Melhor Solução'
TITLE = 'SJC2.dat: ' + X + ' x ' + Y

try:
	os.remove('plot_commands.gp')
	os.remove('graph.png')
except OSError:
    pass

plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

values_best = [0] * 100
values_local = [0] * 100

counter = 0
cur_file = open('0.txt', 'r')
for line in cur_file:
	if 'Best global' in line:
		values_best[counter] += float(line.split()[2])

	if 'Best local' in line:
		values_local[counter] += float(line.split()[2])
		counter += 1

cur_file.close()

best_dat = open('best.dat', 'w')
local_dat = open('local.dat', 'w')
for i in range(len(values_best)):
	best_dat.write(str(i+1) + '\t' + str(values_best[i]) + '\n')
	local_dat.write(str(i+1) + '\t' + str(values_local[i]) + '\n')

best_dat.close()
local_dat.close()

plot_cmds.write('plot ')
plot_cmds.write('\'best.dat\' u 1:2 title \'Global\' smooth bezier, ')
plot_cmds.write('\'local.dat\' u 1:2 title \'Local\' smooth bezier')

plot_cmds.close()
sp.call(['gnuplot', 'plot_commands.gp'])
