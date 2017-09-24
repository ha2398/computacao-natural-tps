#!/usr/bin/env python3

'''
individual.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import math
import numpy as np
import sys

# Types of nodes in the individual tree.
FUN = 'Function'
VAR = 'Variable'
CONST = 'Constant'

NTYPES = [FUN, VAR, CONST]
NUM_TYPES = len(NTYPES)
PROB = [1/(NUM_TYPES) for i in range(NUM_TYPES)]

# Available functions.
PLUS = '+'
MINUS = '-'
MULT = '*'
DIV = '/'
LOG = 'log'
SIN = 'sin'
COS = 'cos'
SQRT = 'sqrt'
POW = '^'

BINARY = [PLUS, MINUS, MULT, DIV, POW]
UNARY = [LOG, SIN, COS, SQRT]

FUNCTIONS_STR = BINARY + UNARY

FUNCTIONS = {
	PLUS: (lambda x, y: np.add(x, y)),
	MINUS: (lambda x, y: np.subtract(x, y)),
	MULT: (lambda x, y: np.multiply(x, y)),
	DIV: (lambda x, y: np.divide(x, y) if y !=0 else 1),
	POW: (lambda x, y: np.power(float(x), float(y)).real),
	LOG: (lambda x: np.log(x) if x > 0 else 1),
	SIN: (lambda x: np.sin(x)),
	COS: (lambda x: np.cos(x)),
	SQRT: (lambda x: np.sqrt(x ** 0.5).real if x >= 0 else 0)
}

# Global parameters

# Maximum and minimum constant values for nodes.
MAX_CONST = 10
MIN_CONST = -10


class Node():

	def __init__(self, etype, element, parent = None, lchild = None,
			rchild = None):
		''' @etype: Type of the node.
			@dlement: Actual element the node holds.
			@lchild: Left child.
			@rchild: Right child.'''

		self.etype = etype
		self.element = element
		self.parent = parent
		self.lchild = lchild
		self.rchild = rchild

	def new_random(parent, num_var, min_const, max_const, prob = PROB,
		ntypes = NTYPES):
		''' Generates a new random Node.
			@num_var: Number of variables the individual tree may contain.
			@min_const: Smallest possible constant value for constant type
			nodes.
			@max_const: Largest possible constant value for constant type nodes.
			@prob: probabilities of choosing each type.
			@ntypes: List with possible node types for the node to be generated.
			@return: A random Node.'''

		ntype = np.random.choice(ntypes, p=prob)

		if (ntype == FUN):
			operator = np.random.choice(FUNCTIONS_STR)
			element = (operator, FUNCTIONS[operator])
		elif (ntype == VAR):
			element = np.random.randint(0, num_var)
		else:
			element = np.random.uniform(min_const, max_const)

		return Node(ntype, element, parent)
	
	def count_subtree(self):
		''' Counts the amount of nodes in this subtree.
			@return: Amount of nodes in this node's subtree (inclusive). '''

		stack = [self]
		count = 0

		while len(stack) != 0:
			count += 1
			node = stack.pop(0)

			if (node.lchild != None):
				stack.append(node.lchild)
			if (node.rchild != None):
				stack.append(node.rchild)

		return count

	def eval(self, x):
		''' Evaluate the node.
			@x: List of values for each variable in the tree.
			@return: The node's resulting value. '''

		etype = self.etype

		if (etype == FUN): # Node is a function.
			right = self.rchild.eval(x)

			if np.isnan(right):
				right = 0
			if right == float('inf'):
				right = sys.maxsize
			if right == float('-inf'):
				right = -1 * sys.maxsize

			operator = self.element[1]
			op_str = self.element[0]

			try:
				if (op_str in UNARY):
					result = operator(right)
					if np.isnan(result):
						return 0
					else:
						return result
				else:
					left = self.lchild.eval(x)

					if np.isnan(left):
						left = 0
					if left == float('inf'):
						left = sys.maxsize
					if left == float('-inf'):
						left = -1 * sys.maxsize

					result = operator(left, right)
					if np.isnan(result):
						return 0
					else:
						return operator(left, right)
			except OverflowError:
				return sys.maxsize
		elif (etype == VAR): # Node is a variable.
			index = self.element
			return x[index]
		else: # Node is a constant.
			return self.element

	def __str__(self):
		''' Creates a string representation of the node.
			@return: string that represents the node. '''

		if self == None:
			return ''
		else:
			if self.etype == FUN:
				left = self.lchild.__str__()
				if left == 'None':
					left = ''
				right = self.rchild.__str__()
				return '(' + left + self.element[0] + right + ')'
			elif self.etype == VAR:
				return '(x' + str(self.element) + ')'
			else:
				return str(self.element)


class Individual():
	
	def __init__(self, root = None, size = 0):
		self.fitness = None
		self.root = root
		self.size = size

	def copy(self):
		''' Returns a copy of itself.
			@return: A new individual which is a copy of self. '''

		original = self.root
		if original == None:
			return None

		copy = Individual(Node(original.etype, original.element, None, None,
			None), self.size)
		
		clone = copy.root

		while original != None:
			if original.lchild != None and clone.lchild == None:
				l = original.lchild
				clone.lchild = Node(l.etype, l.element, clone, None, None)
				original = original.lchild
				clone = clone.lchild
			elif original.rchild != None and clone.rchild == None:
				r = original.rchild
				clone.rchild = Node(r.etype, r.element, clone, None, None)
				original = original.rchild
				clone = clone.rchild
			else:
				original = original.parent
				clone = clone.parent

		return copy

	def get_node(self, index):
		''' Gets a node by index. 
			@index: Index of node to retrieve. 
			@return: Node at given index in the individual. '''

		stack = [self.root]
		current = 0

		while current < index:
			node = stack.pop(0)
			current += 1

			if (node.lchild != None):
				stack.append(node.lchild)

			if (node.rchild != None):
				stack.append(node.rchild)

		return stack.pop(0)

	def eval(self, x):
		''' Evaluate the individual.
			@x: List of values for each variable in the tree.
			@return: The individual's resulting value. '''

		return self.root.eval(x)

	def calculate_fitness(self, x_list, y):
		''' Calculate the individual's fitness.
			@x_list: 2-dimensional list with the variable values for each
			function point. 
			@y: List with the function value for each point.
			@return: Individual's fitness according to its RMSE. '''

		if self.fitness != None:
			return

		n = len(y)
		evals = [self.eval(x) for x in x_list]

		error = []
		for a, b in zip(evals, y):
			try:
				error.append(np.power(a-b, 2))
			except:
				error.append(sys.maxsize)

		result = np.power(((1/n) * sum(error)), 0.5)
		self.fitness = result
		return

	def full(max_depth, num_var):
		''' Creates a new Individual, using the Full method.
			@max_depth: Maximum depth of the Individual trees.
			@num_var: Number of variables the individual tree may contain.
			@return: A random Full Individual. '''

		root = Node.new_random(None, num_var, MIN_CONST, MAX_CONST, [1], [FUN])
		size = 1
		former_level = [root]
		level = []
		depth = 1

		# Fills tree with functions in the non-leaf nodes.
		while depth != max_depth:
			depth += 1

			for node in former_level:
				node.rchild = \
						Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
						[1], [FUN])
				size += 1
				level.append(node.rchild)

				if node.element[0] in BINARY:
					node.lchild = \
						Node.new_random(node, num_var, MIN_CONST, MAX_CONST, [1],
						[FUN])
					size += 1
					level.append(node.lchild)

			former_level = level
			level = []

		# Creates leaf nodes.
		for node in former_level:
			node.rchild = \
				Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
				[0.5, 0.5], [VAR, CONST])

			size += 1

			if node.element[0] in BINARY:
				node.lchild = \
					Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
						[0.5, 0.5], [VAR, CONST])
				size += 1

		return Individual(root, size)

	def grow(max_depth, num_var):
		''' Creates a new Individual, using the Grow method.
			@max_depth: Maximum depth of the Individual trees.
			@num_var: Number of variables the individual tree may contain.
			@return: A random Grow Individual. '''

		grow_probs = [0.8, 0.1, 0.1]

		root = Node.new_random(None, num_var, MIN_CONST, MAX_CONST, grow_probs,
			NTYPES)
		size = 1

		# Pushes to stack the current node and its depth.
		stack = [(root, 0)]

		# Fills tree with random nodes.
		while len(stack) != 0:
			current = stack.pop(0)
			node = current[0]
			depth = current[1]

			# Only expands subtree if the node is of type FUN.
			if node.etype == FUN:
				if (depth + 1) == max_depth: # Next level is leaves level.
					node.rchild = \
						Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
						[0.5, 0.5], [VAR, CONST])
					size += 1
					
					if node.element[0] in BINARY:
						node.lchild = \
							Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
							[0.5, 0.5], [VAR, CONST])

						size += 1
				else:
					node.rchild = \
						Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
							grow_probs, NTYPES)
					size += 1

					if node.element[0] in BINARY:
						node.lchild = \
							Node.new_random(node, num_var, MIN_CONST, MAX_CONST,
								grow_probs, NTYPES)

						size += 1

				stack.append((node.rchild, depth+1))
				if node.element[0] in BINARY:
					stack.append((node.lchild, depth+1))

		return Individual(root, size)

	def ramped_half(psize, max_depth, num_var):
		''' Creates a random population, using the Ramped Half and Half method.
			@psize: Number of individuals in the population.
			@max_depth: Maximum depth of the Individual trees.
			@num_var: Number of variables the individual tree may contain.
			@return: A random population. '''

		amount_each = psize // (max_depth - 1)
		population = []

		for depth in range(2, max_depth+1):
			population_full = [Individual.full(depth, num_var)
				for x in range(amount_each//2)]
			population_grow = [Individual.grow(depth, num_var)
				for x in range(amount_each//2)]

			population = population + population_full + population_grow

		return population

	def __str__(self):
		''' Creates a string representation of the individual.
			@return: string that represents the individual. '''

		return self.root.__str__()
