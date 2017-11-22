#!/usr/bin/env python3

'''
tp3.py: Artificial Neural Networks
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''


import argparse as ap
import numpy as np


# Global variables
parts = ['CYT', 'MIT', 'ME1', 'ME2', 'ME3', 'EXC', 'NUC']
CELL_PARTS = {parts[i]: i for i in range(len(parts))} 


def parse_arguments():
	''' Add command line arguments to the program.

		@return:	Command line arguments.
		@rtype:		argparse.Namespace.
		'''

	parser = ap.ArgumentParser()
	parser.add_argument('input_filename', type=str, help='Name of input file')
	return parser.parse_args()


def read_input(input_filename):
	''' Read input data and format it into data and target arrays.

		@param 	input_filename: Name of the input file.
		@type 	input_filename: String.

		@return: 	Data and target arrays.
		@rtype:		Numpy array, Numpy array.
		'''

	data = []
	target = []
	with open(input_filename, 'r') as input_file:
		for line in input_file:
			line_data = line.strip().split(';')

			data.append([float(x) for x in line_data[:-1]])
			target.append(CELL_PARTS[line_data[-1]])

	return np.array(data), np.array(target)


def main():

	args = parse_arguments()
	data, target = read_input(args.input_filename)

main()