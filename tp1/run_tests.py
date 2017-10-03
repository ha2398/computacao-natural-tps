#!/usr/bin/env python3

'''
run_tests.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import glob as gl
import os
import subprocess as sp


# Constants
TEST_FOLDER = 'test_output'
INPUT_FOLDER = 'datasets'

POP_SIZES = [50, 100, 500] # population sizes
GENS = [50, 100, 500] # number of generations
KTOUR = [3, 7] # tournament k sizes
CROSSR = [0.6, 0.9] # crossover rates
MUTR = [0.3, 0.05] # mutation rates

params_list = ['-p ' + str(p) + ' -k ' + str(k) + \
	' -g ' + str(g) + ' -c ' + str(c) + ' -m ' + str(m) \
	for p in POP_SIZES for g in GENS for k in KTOUR for (c,m) in \
	zip(CROSSR,MUTR)]

sp.call(['rm', '-rf', TEST_FOLDER])
sp.call(['mkdir', TEST_FOLDER])

input_folders = \
	[f for f in os.listdir('./' + INPUT_FOLDER) if not os.path.isfile(f)]

num_tests = len(input_folders) * len(params_list) * 30
cur_test = 0

for folder in input_folders:
	name = TEST_FOLDER + '/' + folder
	sp.call(['mkdir', name])

	for param in params_list:
		name = name + '/' + param
		name = name.replace(' ', '-').replace('--', '-')
		sp.call(['mkdir', name])

		for seed in range(30):
			cur_test += 1
			output_name = name + '/' + str(seed) + '.out'
			output_file = open(output_name, 'w')

			arg_list = [
				'src/tp1.py',
				INPUT_FOLDER + '/' + folder + '/train.csv',
				INPUT_FOLDER + '/' + folder + '/test.csv'] + param.split() + \
				['-s', str(seed)]

			progress = ((cur_test / num_tests) * 100)
			print('(' + str(round(progress, 2)) + '%)', ' '.join(arg_list))
			sp.call(arg_list, stdout = output_file)
			output_file.close()
