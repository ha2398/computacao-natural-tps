#!/usr/bin/env python3

functions = ['+', '-', '/', '*']


class Node():

	def __init__(self, element, lchild = None, rchild = None):
		self.element = element
		self.lchild = lchild
		self.rchild = rchild
	
	def eval(self):
		

class Individual():
	
	def __init__(self):
		self.root = None
	
	def eval(self):
		return self.root.eval()

Node()
