#!/usr/bin/env python3

'''
tp1.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import argparse
import csv

# Adds optional command line arguments to the program.
parser = argparse.ArgumentParser()

parser.add_argument('TRAIN_FILE', metavar='train_file', type=str,
	help='Name of training data file')
parser.add_argument('TEST_FILE', metavar='test_file', type=str,
	help='Name of test data file')

parser.add_argument('-d', dest='MAX_DEPTH', default=7, type=int,
	help='Maximum depth of the individual trees')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Random number generation seed')
parser.add_argument('-p', dest='POP_SIZE', default=54, type=int,
	help='Population size')
parser.add_argument('-k', dest='KTOUR', default=7, type=int,
	help='Number of individuals to be selected using Tournament Selection')
parser.add_argument('-g', dest='NGEN', default=10, type=int,
	help='Number of generations to run the program for')

args = parser.parse_args()

# Random numbers generation setup.
import random
random.seed(args.RSEED)

import individual as ind
import gp


################################################################################


def list_from_csv(filename):
	''' Gets a list of lists from a CSV file.
		@filename: CSV file name;
		@return: List of lists with the file's content. '''
	file = open(filename, 'r')
	reader = csv.reader(file ,quoting=csv.QUOTE_NONNUMERIC)
	csv_list = list(reader)
	file.close()

	return csv_list


def main():
	''' Main function. '''

	# Obtains the input data.
	train_data = list_from_csv(args.TRAIN_FILE)
	train_xs = [x[:-1] for x in train_data]
	train_y = [x[-1] for x in train_data]

	test_data = list_from_csv(args.TEST_FILE)
	test_xs = [x[:-1] for x in test_data]
	test_y = [x[-1] for x in test_data]

	num_var = len(train_xs[0]) - 1

	population = ind.Individual.ramped_half(args.POP_SIZE, args.MAX_DEPTH, \
		num_var)

	# Main GP loop.
	for generation in range(args.NGEN):
		# Selects individuals to be parents of the next generation.
		parent1 = \
			gp.tournament_selection(population, args.KTOUR, train_xs, train_y)

		parent2 = \
			gp.tournament_selection(population, args.KTOUR, train_xs, train_y)

		# Elitism.
		#population = [parent1, parent2]




main()