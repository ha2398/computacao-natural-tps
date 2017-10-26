#!/usr/bin/env python3

'''
tp2.py: Main program
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import aco
import argparse
import client as cli

# Add optional command line arguments to the program
parser = argparse.ArgumentParser()

parser.add_argument('INPUT_FILE', type=str, help='Name of input file')

parser.add_argument('-a', dest='ANTN', default=4, type=int,
	help='Number of ants')
parser.add_argument('-i', dest='MAXIT', default=10, type=int,
	help='Number of iterations to run the program for')

args = parser.parse_args()

################################################################################


def get_data(filename):
	''' Read data from file.

		@param	filename:	Name of the file to read data from.
		@type	filename:	String.

		@return:	Number p of medians and list clients with all clients found
					in input file. Each client has the format (x, y, c, d),
					where x	is the x coordinate, y is the y coordinate, c is the
					client's capacity and d its demand.
		'''

	input_file = open(filename, 'r')

	p = int(input_file.readline().split()[1])
	clients = []

	for line in input_file:
		data = line.split()

		x = float(data[0])
		y = float(data[1])
		c = float(data[2])
		d = float(data[3])

		clients.append(cli.Client(x, y, c, d))

	input_file.close()

	return p, clients


def main():
	p, clients = get_data(args.INPUT_FILE)
	p_medians = aco.ACO(p, clients)


################################################################################


main()