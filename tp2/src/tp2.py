#!/usr/bin/env python3

'''
tp2.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import argparse

# Add optional command line arguments to the program
parser = argparse.ArgumentParser()

parser.add_argument('INPUT_FILE', type=str, help='Name of input file')

args = parser.parse_args()

################################################################################


def get_data(filename):
	''' Read data from file.

		@filename:	Name of the file to read data from.
		@return:	Number p of medians and list points with all points found in
					input file. Each point has the format (x, y, c, d), where x
					is the x coordinate, y is the y coordinate, c is the point's
					capacity and d its demand.
		'''

	input_file = open(filename, 'r')

	p = int(input_file.readline().split()[1])
	points = []

	for line in input_file:
		data = line.split()

		x = float(data[0])
		y = float(data[1])
		c = float(data[2])
		d = float(data[3])

		points.append((x, y, c, d))

	return p, points


def main():
	p, points = get_data(args.INPUT_FILE)


################################################################################


main()