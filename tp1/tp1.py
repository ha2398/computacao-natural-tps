'''
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

# Types of nodes in the individual tree.
FUN = 'function'
VAR = 'variable'
CONST = 'constant'

# Available functions.
PLUS = '+'
MINUS = '-'
MULT = '*'
DIV = '/'

FUNCTIONS = {
	PLUS: (lambda x, y: x + y),
	MINUS: (lambda x, y: x + y),
	MULT: (lambda x, y: x * y),
	DIV: (lambda x, y: x / y),
}


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
	
	def eval(self, x):
		''' Evaluate the node.
			@x: List of values for each variable in the tree.
			@return: The node's resulting value. '''
		etype = self.etype

		if (etype == FUN): # Node is a function.
			left = self.lchild.eval(x)
			right = self.rchild.eval(x)
			operator = self.element
			return FUNCTIONS[operator](left, right)
		elif (etype == VAR): # Node is a variable.
			index = self.element
			return x[index]
		else: # Node is a constant.
			return self.element


class Individual():
	
	def __init__(self, root = None):
		self.root = root
	
	def eval(self, x):
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
		

a = Individual(Node(FUN, MULT, Node(VAR, 1), Node(CONST, 8)))
x_list = [range(3), range(1,4), range(2,5)]
y = [4, 0, 2]
x = [8, 4, 1]

print(a.fitness(x_list, y))