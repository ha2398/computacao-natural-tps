#!/usr/bin/env python3

'''
tp2.py: Main program
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import aco
import argparse
import client as cli
import numpy as np

# Add optional command line arguments to the program
parser = argparse.ArgumentParser()

parser.add_argument('INPUT_FILE', type=str, help='Name of input file')

parser.add_argument('-n', dest='ANTN', default=4, type=int,
	help='Number of ants')
parser.add_argument('-i', dest='MAXIT', default=10, type=int,
	help='Number of iterations to run the program for')
parser.add_argument('-d', dest='DECAYR', default=0.25, type=float,
	help='Pheromone decay rate')
parser.add_argument('-a', dest='ALPHA', default=3, type=int,
	help='Weight of trail intensity')
parser.add_argument('-b', dest='BETA', default=1, type=int,
	help='Weight of information heuristic')

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

	with open(filename, 'r') as input_file:
		p = int(input_file.readline().split()[1])

		count = 0
		clients = []
		for line in input_file:
			clients.append(cli.Client(count, *line.split()))

		return p, clients

def main():
	p, clients = get_data(args.INPUT_FILE)
	p_medians = aco.ACO(p, clients, args.MAXIT, args.ANTN, args.DECAYR,
		args.ALPHA, args.BETA)
	p_medians.ant_system()

	a = p_medians.sort_nodes(2)
	print(a)


################################################################################


main()