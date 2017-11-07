#!/usr/bin/env python3

import os
import subprocess as sp

X = 'Iteração'
Y = 'Ótimo Global'
TITLE = 'SJC2.dat: ' + X + ' x ' + Y

try:
	os.remove('plot_commands.gp')
	os.remove('graph.png')
except OSError:
    pass

folders = sorted([f for f in os.listdir('./') if not os.path.isfile(f)])

plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

for folder in folders:
	files = [f for f in os.listdir('./' + folder)]
	values = [0] * 50

	for file in files:
		counter = 0
		cur_file = open('./' + folder + '/' + file, 'r')
		for line in cur_file:
			if 'Best global' in line:
				values[counter] += float(line.split()[2])
				counter += 1
		cur_file.close()

	values = [(x/len(files)) for x in values]

	dat = open(folder + '.txt', 'w')
	for i in range(len(values)):
		dat.write(str(i+1) + '\t' + str(values[i]) + '\n')

	dat.close()


plot_cmds.write('plot ')
for i in range(len(folders)):
	plot_cmds.write('\'' + folders[i] + '.txt\' u 1:2 title \'' + folders[i] + '\' smooth bezier')
	if i != len(folders) - 1:
		plot_cmds.write(', ')

plot_cmds.close()
sp.call(['gnuplot', 'plot_commands.gp'])
