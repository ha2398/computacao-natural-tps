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

parser.add_argument('TRAIN_FILE', metavar='train', type=str,
	help='Name of training data file')
parser.add_argument('TEST_FILE', metavar='test', type=str,
	help='Name of test data file')

parser.add_argument('-d', dest='MAX_DEPTH', default=7, type=int,
	help='Maximum depth of the individual trees')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Random number generation seed')
parser.add_argument('-p', dest='POP_SIZE', default=0, type=int,
	help='Population size')

args = parser.parse_args()

# Random numbers generation setup.
import random
random.seed(args.RSEED)

import individual as ind


################################################################################


def list_from_csv(filename):
	''' Gets a list of lists from a CSV file.
		@filename: CSV file name;
		@return: List of lists with the file's content. '''
	file = open(filename, 'r')
	reader = csv.reader(file)
	csv_list = list(reader)
	file.close()

	return csv_list


def main():
	''' Main function. '''

	# Obtains the input data.
	train_data = list_from_csv(args.TRAIN_FILE)
	test_data = list_from_csv(args.TEST_FILE)

	num_var = len(train_data[0]) - 1

	population = ind.Individual.ramped_half(args.POP_SIZE, args.MAX_DEPTH, \
		num_var)

	for individual in population:
		print(individual)


main()