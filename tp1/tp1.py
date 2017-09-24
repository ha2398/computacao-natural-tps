#!/usr/bin/env python3

'''
tp1.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import argparse
import csv
import numpy as np
import sys
import time

# Adds optional command line arguments to the program.
parser = argparse.ArgumentParser()

parser.add_argument('TRAIN_FILE', metavar='train_file', type=str,
	help='Name of training data file')
parser.add_argument('TEST_FILE', metavar='test_file', type=str,
	help='Name of test data file')

parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Random number generation seed')
parser.add_argument('-p', dest='POP_SIZE', default=54, type=int,
	help='Population size')
parser.add_argument('-k', dest='KTOUR', default=7, type=int,
	help='Number of individuals to participate in tournaments')
parser.add_argument('-g', dest='NGEN', default=10, type=int,
	help='Number of generations to run the program for')
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

# Constants
MAX_DEPTH = 7
ELIT_SIZE = 2
REPR = 1 - (args.CROSSR + args.MUTR)


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


def evaluate_test_data(population, n, test_xs, test_y):
	''' Evaluates the top n individuals in a population using the test dataset.
		@population: List of individuals from which to get the top n.
		@n: Number of individuals to evaluate.
		@test_xs: the list of x test inputs.
		@test_y: The list of y outputs for each test_xs entry.
		@return: The top n individuals, sorted from best to worst. '''

	gp.evaluate_population(population, test_xs, test_y)
	topn = sorted(population, key=lambda x: (x.fitness, x.size))[0:n]
	return topn


def main():
	''' Main function. '''
	np.seterr(all='ignore')

	p_start = time.time()

	GEN_OP_PROB = [args.CROSSR, args.MUTR, args.REPR]

	# Obtains the input data.
	train_xs, train_y = get_data(args.TRAIN_FILE)
	test_xs, test_y = get_data(args.TEST_FILE)

	num_var = len(train_xs[0])

	# Generates initial population.
	population = ind.Individual.ramped_half(args.POP_SIZE, MAX_DEPTH,
		num_var)

	# Evaluate the individuals.
	gp.evaluate_population(population, train_xs, train_y)
	gp.penalize_large_ind(population, (2**MAX_DEPTH)-1)
	best = gp.get_best(population)
	pop_str = [x.__str__() for x in population]

	# Main loop
	for x in range(args.NGEN):
		crossover_offspring = 0
		crossover_improved = 0
		mutation_offspring = 0
		mutation_improved = 0

		# Generates new population.
		children = []
		while len(children) < (args.POP_SIZE - ELIT_SIZE):
			operator = gp.select_genetic_operator(GEN_OP_PROB)

			if (operator == gp.CROSS): # Crossover
				parent1 = gp.tournament_selection(population, args.KTOUR)
				parent2 = gp.tournament_selection(population, args.KTOUR)
				offspring = gp.subtree_crossover(parent1, parent2)

				# Gets statistics.
				crossover_offspring += 2
				gp.evaluate_population(offspring, train_xs, train_y)
				for child in offspring:
					fit = child.fitness
					if 	fit < parent1.fitness or fit < parent2.fitness:
						crossover_improved += 1

				children = children + offspring
			elif (operator == gp.MUTAT): # Mutation
				parent = gp.tournament_selection(population, args.KTOUR)
				mutants = gp.mutation(parent, num_var)

				# Gets statistics.
				mutation_offspring += 2
				gp.evaluate_population(mutants, train_xs, train_y)
				for mutant in mutants:
					if mutant.fitness < parent.fitness:
						mutation_improved += 1

				children = children + mutants
			else: # Reproduction
				children.append(gp.reproduction(population))

		# Elitism
		for i in range(ELIT_SIZE):
			children.append(gp.reproduction(population))

		gp.evaluate_population(children, train_xs, train_y)
		gp.penalize_large_ind(population, (2**MAX_DEPTH)-1)
		population = children
		pop_str = [x.__str__() for x in population]
		best = gp.get_best(population)

		if mutation_offspring != 0:
			mutation_improvement_rate = \
				str(round((mutation_improved/mutation_offspring)*100, 2)) + '%'
		else:
			mutation_improvement_rate = '0.0%'

		if crossover_offspring != 0:
			crossover_improvement_rate = \
				str(round((crossover_improved/crossover_offspring)*100,2)) + '%'
		else:
			crossover_improvement_rate = '0.0%'

		print('Generation', x+1)
		print('Best fitness:', best.fitness)
		print('Worst fitness:', gp.get_worst(population).fitness)
		print('Average fitness:', gp.get_average_fitness(population))
		print('Number of repeated individuals:', len(pop_str)-len(set(pop_str)))
		print('Mutation improvement rate:', mutation_improvement_rate)
		print('Crossover improvement rate:', crossover_improvement_rate)
		print()

	# Results
	n = 5
	print('Top', n, 'individuals for training dataset:\n')
	population.sort(key=lambda x: (x.fitness, x.size))
	for individual in population[0:n]:
		print('\t', individual, '\tFitness:', individual.fitness)

	# Tests best individuals with test dataset.
	topn = evaluate_test_data(population, n, test_xs, test_y)
	print('\nTop', n, 'individuals for test dataset:\n')
	for individual in topn:
		print('\t', individual, '\tFitness:', individual.fitness)


################################################################################


main()