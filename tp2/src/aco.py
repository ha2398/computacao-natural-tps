#!/usr/bin/env python3

'''
aco.py: Ant Colony Optimization 
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import numpy as np

class ACO():
	''' Defines an instance of the Ant Colony Optimization problem.
		
		Attributes:

		@attribute 	p:	Number of medians.
		@type		p:	Integer.

		@attribute 	clients:	Clients.
		@type 		clients:	List of Client.

		@attribute 	d: 	Matrix of distances.		
		@type:		d:	List of List of Float.

		@attribute 	n: 	Number of clients.
		@type:		d:	Integer.

		@attribute 	x: 	Allocation matrix.
		@type		x:	List of List of Integer.

		@attribute 	y:	Median selection vector.
		@type 		y: 	List of Integer.
		'''

	def __init__(self, p, clients):
		''' Initializes an instance of the Ant Colony Optimization Problem.
		
			@param	p:	Number of medians.
			@type	p:	Integer.

			@param	clients:	Clients.
			@type 	clients:	List of Client.
			'''

		self.p = p
		self.clients = clients
		self.d = ACO.build_distance_matrix(clients)

		self.n = len(clients)

		# x_ij = 1 if node i is allocated to median j, 0 otherwise
		self.x = np.zeros((self.n, self.n))

		# y_j = 1 if node j is a median, 0 otherwise
		self.y = np.zeros(self.n)

		self.pheromone = np.full(self.n, 0.5)

	def build_distance_matrix(clients):
		''' Build distance matrix D where Dij indicates the distance between
			client i and j.

			@param	clients:	List with all clients.
			@type	clients:	List of Client.

			@return:		Matrix D of distances.		
			@rtype:			List of List of Float.
			'''



		size = len(clients)
		D = np.zeros((size, size))

		for i in range(size):
			for j in range(i, size):
				D[i][j] = D[j][i] = clients[i].distance(clients[j])

		return D