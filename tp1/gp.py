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


def subtree_crossover(parent1, parent2): # TODO
	''' Given two parents, produces two new individuals using the subtree
		crossover method.
		@parent1: First parent.
		@parent2: Second parent.
		@return: A list with the parent's offspring. '''

	child1 = parent1.copy()
	child2 = parent2.copy()

	crossover_point1 = np.random.choice(list(range(child1.size)))
	crossover_point2 = np.random.choice(list(range(child2.size)))

	node1 = child1.get_node(crossover_point1)
	node2 = child2.get_node(crossover_point2)

	parent1 = node1.parent
	parent2 = node2.parent

	# Swap subtrees
	# Moves Node 1 to Child 2.
	if (node2.parent == None): # Node 2 is root.
		child2.root = node1
	else: # Node 2 isn't root.
		if (node2.parent.lchild == node2): # Node 2 is left child.
			node2.parent.lchild = node1
		else: # Node 2 is right child.
			node2.parent.rchild = node1

	# Moves Node 2 to Child 1.
	if (node1.parent == None): # Node 1 is root.
		child1.root = node2
	else: # Node 1 isn't root.
		if (node1.parent.lchild == node1): # Node 1 is left child.
			node1.parent.lchild = node2
		else:
			 # Node 1 is right child.
			 node1.parent.rchild = node2

	node1.parent = parent2
	node2.parent = parent1

	# Updates sizes
	child1.size = child1.root.count_subtree()
	child2.size = child2.root.count_subtree()

	return [child1, child2]


def reproduction(population):
	''' Reproduces the best individual to the next generation.
		@population: Population that contains the individual.
		@return: The best individual from the given population. '''

	best = get_best(population)
	population.remove(best)
	return best