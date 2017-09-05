'''
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''


functions = {
	'+': (lambda x, y: x + y),
	'-': (lambda x, y: x + y),
	'*': (lambda x, y: x * y),
	'/': (lambda x, y: x / y)
}


class Node():

	def __init__(self, element, lchild = None, rchild = None):
		self.element = element
		self.lchild = lchild
		self.rchild = rchild
	
	def eval(self):
		if (self.lchild == None or self.rchild == None):
			return self.element
		else:
			return functions[self.element](self.lchild.eval(), self.rchild.eval())


class Individual():
	
	def __init__(self):
		self.root = None
	
	def eval(self):
		return self.root.eval()

