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
		@type 		clients:	Numpy Array of Client.

		@attribute 	d: 	Matrix of distances.		
		@type:		d:	Numpy Array of Numpy Array of Float.

		@attribute 	n: 	Number of clients.
		@type:		d:	Integer.

		@attribute 	x: 	Allocation matrix.
		@type		x:	Numpy Array of Numpy Array of Integer.

		@attribute 	y:	Median selection vector.
		@type 		y: 	Numpy Array of Integer.

		@attribute 	pheromone: 	Pheromone vector.
		@type 		pheromone:	Numpy Array of Float.
		'''

	def __init__(self, p, clients, maxit, antn, decayr, alpha, beta):
		''' Initializes an instance of the Ant Colony Optimization Problem.
		
			@param	p:	Number of medians.
			@type	p:	Integer.

			@param	clients:	Clients.
			@type 	clients:	Numpy Array of Client.

			@param 	maxit: 	Number of iterations to run the program for.
			@type 	maxit: 	Integer.

			@param 	antn: 	Number of ants.
			@type 	antn: 	Integer.

			@param 	decayr: Pheromone decay rate.
			@type 	decayr: Float.

			@param 	alpha: 	Information heuristic alpha parameter.
			@type 	alpha: 	Float.

			@param 	beta: 	Information heuristic beta parameter.
			@type 	beta: 	Float.
			'''

		self.p = p
		self.clients = clients
		self.maxit = maxit
		self.antn = antn
		self.decayr = decayr
		self.alpha = alpha
		self.beta = beta

		self.d = ACO.build_distance_matrix(clients)

		self.n = len(clients)

		# x_ij = 1 if node i is allocated to median j, 0 otherwise
		self.x = np.zeros((self.n, self.n))

		# y_j = 1 if node j is a median, 0 otherwise
		self.y = np.zeros(self.n)

		self.pheromone = np.full(self.n, 0.5)

		# For each ant, stores solution cost and medians chosen.
		self.costs = np.zeros(self.antn)
		self.medians = np.full((self.antn, 1), np.array([0]))

	def evaluate_solution(self):
		''' Return the cost of the current solution.
			'''

		cost = 0
		for i in range(self.n):
			for j in range(self.n):
				cost += self.d[i, j] * self.x[i, j]

		return cost

	def build_solution(self):
		''' Build a solution to the problem using the current pheromone
			setting and ants.
			'''

	def update_pheromone(self):
		'''	Update pheromone vector based on the paths the ants are using to
			build solutions. 
			'''

	def ant_system(self):
		''' Run the Ant System algorithm.
			'''

		for it in range(self.maxit):
			for ant in range(self.antn):
				self.build_solution()
			
			self.update_pheromone()

	def build_distance_matrix(clients):
		''' Build distance matrix D where Dij indicates the distance between
			client i and j.

			@param	clients:	Numpy Array with all clients.
			@type	clients:	Numpy Array of Client.

			@return:		Matrix D of distances.		
			@rtype:			Numpy Array of Numpy Array of Float.
			'''

		size = len(clients)
		D = np.zeros((size, size))

		for i in range(size):
			for j in range(i, size):
				D[i][j] = D[j][i] = clients[i].distance(clients[j])

		return D