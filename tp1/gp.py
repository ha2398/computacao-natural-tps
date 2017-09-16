#!/usr/bin/env python3

'''
gp.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import copy as cp
import individual as ind
import operator as op
import numpy as np

# Genetic operators
CROSS = 'Crossover'
MUTAT = 'Mutation'
REPROD = 'Reproduction'

GEN_OP = [CROSS, MUTAT, REPROD]

def select_genetic_operator(probs):
	''' Selects a genetic operator based on a list of probabilities.
		@probs: List of probabilities for each operator.
		@return: String that represents the operator. '''

	return np.random.choice(GEN_OP, p=probs) 


def evaluate_population(population, xs, y):
	''' Calculates the fitness of each individual.
		@population: Collection of individuals to calculate the fitness of.
		@xs: List of inputs for the individual.
		@y: List of correct outputs for each of the inputs in @xs. '''

	for individual in population:
		individual.calculate_fitness(xs, y)


def get_best(population):
	''' Returns the best individual in a given population. 
		@population: Population to search in.
		@return: The best individual found. '''

	best = min(population, key=op.attrgetter('fitness'))
	return best


def tournament_selection(population, k):
	''' Randomly selects k individuals out of a population and returns the one
		with the best fitness.
		@population: List of individuals to select from. 
		@k: Number of individuals to participate in the tournament.
		@return: The best individual out of the k ones initially selected. '''

	np.random.shuffle(population)
	selected = population[0:k]

	return get_best(selected)


def subtree_crossover(parent1, parent2):
	''' Given two parents, produces two new individuals using the subtree
		crossover method.
		@parent1: First parent.
		@parent2: Second parent.
		@return: A list with the parent's offspring. '''

	child1 = cp.deepcopy(parent1)
	child2 = cp.deepcopy(parent2)