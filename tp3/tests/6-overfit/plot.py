#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from subprocess import call

X = 'Partição'
Y = 'Acurácia'
TITLE = X + ' x ' + Y

try:
	call(['rm', '-rf', 'plot_commands.gp'])
	call(['rm', '-rf', 'graph.png'])
	call(['rm', '-rf', '*.dat*'])
except OSError:
    pass

# Get all files
files = [file for file in listdir('./') if '.out' in file]
folds = 0
train = [0] * 3
test = [0] * 3

# For each file
for f in files:
	file = open(join('./', f), 'r')
	fold = 0

	for line in file:
		if 'acc' in line:
			new_train = float(line[6:-2].split(', ')[-1])
			train[fold] += new_train

		if 'test' in line:
			new_test = float(line[7:-2].split(', ')[-1])
			test[fold] += new_test
			fold += 1

	file.close()

# Calculate the means
# Save them in a .dat file (one .dat file per folder)
dat = open('data.dat', 'w')
for i in range(len(train)):
	train[i] /= len(files)
	test[i] /= len(files)
	dat.write(str(i+1) + '\t' + str(train[i]) + '\t' + str(test[i]) + '\n')

dat.close()

# Plot all of them in a single plot
plot_cmds = open('plot_commands.gp', 'w')
plot_cmds.write('set terminal png ')
plot_cmds.write('size 1200,900\n')
plot_cmds.write('set output \'graph.png\'\n')
plot_cmds.write('set title \'{}\'\n'.format(TITLE))
plot_cmds.write('set xlabel \'{}\'\n'.format(X))
plot_cmds.write('set ylabel \'{}\'\n'.format(Y))

plot_cmds.write('red = \"#FF0000\"; green = \"#00FF00\"; blue = \"#0000FF\"; skyblue = \"#87CEEB\";\n')
plot_cmds.write('set yrange [0:1]\n')
plot_cmds.write('set style data histogram\n')
plot_cmds.write('set style histogram cluster gap 1\n')
plot_cmds.write('set style fill solid\n')
plot_cmds.write('set boxwidth 0.9\n')
plot_cmds.write('set xtics format \"\"\n')
plot_cmds.write('set grid ytics\n')


plot_cmds.write('plot \'data.dat\' ')

plot_cmds.write('using 2:xtic(1) title \"Treino\" linecolor rgb red, \\\n'.format(i))
plot_cmds.write('\'\' using 3 title \"Teste\" linecolor rgb blue')


plot_cmds.close()
call(['gnuplot', 'plot_commands.gp'])