'''
individual.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import random

# Types of nodes in the individual tree.
FUN = 'Function'
VAR = 'Variable'
CONST = 'Constant'

NTYPES = [FUN, VAR, CONST]

# Available functions.
PLUS = '+'
MINUS = '-'
MULT = '*'
DIV = '/'

FUNCTIONS = {
	PLUS: (lambda x, y: x + y),
	MINUS: (lambda x, y: x + y),
	MULT: (lambda x, y: x * y),
	DIV: (lambda x, y: x / y if y !=0 else 1),
}

# Global parameters

# Maximum and minimum constant values for nodes.
MAX_CONST = 100
MIN_CONST = -100


class Node():

	def __init__(self, etype, element, lchild = None, rchild = None):
		''' @etype: Type of the node.
			@dlement: Actual element the node holds.
			@lchild: Left child.
			@rchild: Right child.'''

		self.etype = etype
		self.element = element
		self.lchild = lchild
		self.rchild = rchild

	def new_random(num_var, min_const, max_const, ntypes = NTYPES):
		''' Generates a new random Node.
			@num_var: Number of variables the individual tree may contain.
			@min_const: Smallest possible constant value for constant type
			nodes.
			@max_const: Largest possible constant value for constant type nodes.
			@ntypes: List with possible node types for the node to be generated.
			@return: A random Node.'''

		ntype = random.choice(ntypes)

		if (ntype == FUN):
			element = random.choice(list(FUNCTIONS.items()))[1]
		elif (ntype == VAR):
			element = random.randint(0, num_var-1)
		else:
			element = random.uniform(min_const, max_const)

		return Node(ntype, element)
	
	def eval(self, x):
		''' Evaluate the node.
			@x: List of values for each variable in the tree.
			@return: The node's resulting value. '''

		etype = self.etype

		if (etype == FUN): # Node is a function.
			left = self.lchild.eval(x)
			right = self.rchild.eval(x)
			operator = self.element
			return operator(left, right)
		elif (etype == VAR): # Node is a variable.
			index = self.element
			return x[index]
		else: # Node is a constant.
			return self.element


class Individual():
	
	def __init__(self, root = None):
		self.root = root
	
	def eval(self, x):
		''' Evaluate the individual.
			@x: List of values for each variable in the tree.
			@return: The individual's resulting value. '''

		return self.root.eval(x)

	def fitness(self, x_list, y):
		''' Calculate the individual's fitness.
			@x_list: 2-dimensional list with the variable values for each
			function point. 
			@y: List with the function value for each point.
			@return: Individual's fitness according to its RMSE. '''

		n = len(y)
		evals = [self.eval(x) for x in x_list]
		error = [(a - b)**2 for a,b in zip(evals, y)]
		return ((1/float(n)) * sum(error)) ** 0.5

	def full(max_depth, num_var):
		''' Creates a new Individual, using the Full method.
			@max_depth: Maximum depth of the Individual trees.
			@num_var: Number of variables the individual tree may contain.
			@return: A random Full Individual. '''

		root = Node.new_random(num_var, MIN_CONST, MAX_CONST, [FUN])
		former_level = [root]
		level = []
		depth = 1

		# Fills tree with functions in the non-leaf nodes.
		while depth != max_depth:
			depth += 1

			for node in former_level:
				left = Node.new_random(num_var, MIN_CONST, MAX_CONST, [FUN])
				right = Node.new_random(num_var, MIN_CONST, MAX_CONST, [FUN])
				node.lchild = left
				node.rchild = right
				level.append(left)
				level.append(right)

			former_level = level
			level = []

		# Creates leaf nodes.
		for node in former_level:
			left = Node.new_random(num_var, MIN_CONST, MAX_CONST, [VAR, CONST])
			right = Node.new_random(num_var, MIN_CONST, MAX_CONST, [VAR, CONST])
			node.lchild = left
			node.rchild = right

		return Individual(root)