#!/usr/bin/env python3

'''
gp.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

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

	best = max(selected, key=op.attrgetter('last_fitness'))

	return best