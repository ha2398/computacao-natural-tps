#!/usr/bin/env python3

'''
gp.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import copy as cp
import individual as ind
import operator as op
import random

def tournament_selection(population, k, xs, y):
	''' Randomly selects k individuals out of a population and returns the one
		with the best fitness.
		@population: List of individuals to select from. 
		@k: Number of individuals to participate in the tournament.
		@xs: List of inputs for the individual.
		@y: List of correct outputs for each of the inputs in @xs.
		@return: The best individual out of the k ones initially selected. '''
	random.shuffle(population)
	selected = population[0:k]

	for candidate in selected:
		candidate.fitness(xs, y)

	best = min(selected, key=op.attrgetter('last_fitness'))

	return best

def pick_crossover_subtree(individual):
	''' Selects a random individual subtree to perform subtree crossover.
		@individual: Individual to crossover.
		@return: A random Node to crossover. '''
	

def subtree_crossover(parent1, parent2):
	''' Given two parents, produces two new individuals using the subtree
		crossover method.
		@parent1: First parent.
		@parent2: Second parent.
		@return: A list with the parent's offspring. '''
	child1 = cp.deepcopy(parent1)
	child2 = cp.deepcopy(parent2)

