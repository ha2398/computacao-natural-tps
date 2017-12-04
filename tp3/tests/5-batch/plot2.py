#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from subprocess import call

X = 'Tamanho de Batch'
Y = 'Tempo de treinamento (s)'
TITLE = X + ' x ' + Y

try:
	call(['rm', '-rf', 'plot_commands.gp'])
	call(['rm', '-rf', 'graph2.png'])
	call(['rm', '-rf', '*.dat*'])
except OSError:
    pass

# For each folder
folders = sorted([folder for folder in listdir('./') \
	if not isfile(join('./', folder))], key=lambda x: float(x))

for folder in folders:
	# Get all files
	files = [file for file in listdir(join('./', folder)) if '.out' in file]
	folds = 0
	value = 0

	# For each file
	for f in files:
		file = open(join('./', folder, f), 'r')

		for line in file:
			if 'time' in line:
				fold_value = float(line.split(': ')[1])
				folds += 1

				value += fold_value

		file.close()
	
	# Calculate the means
	# Save them in a .dat file (one .dat file per folder)
	dat = open(join('./', folder + '.dat'), 'w')
	value /= folds
	dat.write(folder + '\t' + str(value) + '\n')
	dat.close()

# Plot all of them in a single plot
plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph2.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))
plot_cmds.write('set boxwidth 8.0\n')
plot_cmds.write('set style fill solid\n')
plot_cmds.write('set xrange [-5:110]\n')


plot_cmds.write('plot ')

for i in range(len(folders)):
	plot_cmds.write('\'{}.dat\' u 1:2:xtic(1) notitle with boxes'.format(folders[i],
		folders[i]))

	if i < len(folders) - 1:
		plot_cmds.write(', ')

plot_cmds.close()
call(['gnuplot', 'plot_commands.gp'])