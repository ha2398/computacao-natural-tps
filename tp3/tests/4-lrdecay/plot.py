#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from subprocess import call

X = 'Época'
Y = 'Acurácia'
TITLE = X + ' x ' + Y + ' (por decaimento de taxa de aprendizado)'

try:
	call(['rm', '-rf', 'plot_commands.gp'])
	call(['rm', '-rf', 'graph.png'])
	call(['rm', '-rf', '*.dat*'])
except OSError:
    pass

# For each folder
folders = sorted([folder for folder in listdir('./') \
	if not isfile(join('./', folder))], key=lambda x: float(x))

for folder in folders:
	# Get all files
	files = [file for file in listdir(join('./', folder)) if '.out' in file]
	values = None
	folds = 0

	# For each file
	for f in files:
		file = open(join('./', folder, f), 'r')

		for line in file:
			if 'acc' in line:
				fold_values = [float(x) for x in line.split(', ')[6:-1]]
				folds += 1

				if values == None:
					values = fold_values
				else:
					for i in range(len(values)):
						values[i] += fold_values[i]

		file.close()
	
	# Calculate the means
	# Save them in a .dat file (one .dat file per folder)
	dat = open(join('./', folder + '.dat'), 'w')
	for i in range(len(values)):
		values[i] /= folds

		dat.write(str(i+1) + ', ' + str(values[i]) + '\n')

	dat.close()

# Plot all of them in a single plot
plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))
plot_cmds.write('plot ')


for i in range(len(folders)):
	plot_cmds.write('\'{}.dat\' u 1:2 title \'{}\' smooth bezier'.format(
		folders[i], folders[i]))

	if i < len(folders) - 1:
		plot_cmds.write(', ')

plot_cmds.close()
call(['gnuplot', 'plot_commands.gp'])