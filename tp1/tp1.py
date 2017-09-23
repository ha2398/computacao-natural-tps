#!/usr/bin/env python3

'''
tp1.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import argparse
import csv
import sys
import time

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
	help='Number of individuals to participate in tournaments')
parser.add_argument('-g', dest='NGEN', default=10, type=int,
	help='Number of generations to run the program for')
parser.add_argument('-o', dest='OUTFILE', default='stdout', type=str,
	help='Output file name')
parser.add_argument('-c', dest='CROSSR', default=0.9, type=float,
	help='Crossover rate')
parser.add_argument('-m', dest='MUTR', default=0.05, type=float,
	help='Mutation rate')
parser.add_argument('-r', dest='REPR', default=0.05, type=float,
	help='Reproduction rate')

args = parser.parse_args()

# Random numbers generation setup.
import numpy as np
np.random.seed(args.RSEED)

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


def get_data(filename):
	''' Reads data from file.
		@filename: File to read data from.
		@return:
			@data_xs: the list of x inputs of the original function.
			@data_y: The list of y outputs for each data_xs entry.'''
	
	data = list_from_csv(filename)
	data_xs = [x[:-1] for x in data]
	data_y = [x[-1] for x in data]
	return data_xs, data_y


def main():
	''' Main function. '''

	GEN_OP_PROB = [args.CROSSR, args.MUTR, args.REPR]

	# Obtains the input data.
	train_xs, train_y = get_data(args.TRAIN_FILE)
	test_xs, test_y = get_data(args.TEST_FILE)

	num_var = len(train_xs[0])

	# Generates initial population.
	population = ind.Individual.ramped_half(args.POP_SIZE, args.MAX_DEPTH,
		num_var)

	# Evaluate the individuals.
	gp.evaluate_population(population, train_xs, train_y)

	best = gp.get_best(population)

	# Main loop
	generation = 1
	for x in range(args.NGEN):
		start = time.time()
		print(best.fitness)
		# Elitism
		children = [gp.reproduction(population)]

		# Generates new population.
		while len(children) < args.POP_SIZE:
			operator = gp.select_genetic_operator(GEN_OP_PROB)

			if (operator == gp.CROSS): # Crossover
				parent1 = gp.tournament_selection(population, args.KTOUR)
				parent2 = gp.tournament_selection(population, args.KTOUR)
				children = children + gp.subtree_crossover(parent1, parent2)
			elif (operator == gp.MUTAT): # Mutation
				pass
			else: # Reproduction
				children.append(gp.reproduction(population))

		gp.evaluate_population(children, train_xs, train_y)
		population = children
		generation += 1
		best = gp.get_best(population)
		end = time.time()
		print(end-start)
		print()

	print(best)


################################################################################

main()