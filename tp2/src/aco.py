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
		@type:		d:	Numpy Array of Numpy Array of Float.

		@attribute 	n: 	Number of clients.
		@type:		n:	Integer.

		@attribute 	x: 	Allocation matrix.
		@type		x:	Numpy Array of Numpy Array of Integer.

		@attribute 	y:	Median selection vector.
		@type 		y: 	Numpy Array of Integer.

		@attribute 	pheromone: 	Pheromone vector.
		@type 		pheromone:	Numpy Array of Float.

		@attribute 	costs:	Cost of each solution for each ant.
		@type		costs:	Numpy Array of Float.

		@attribute 	medians:	Medians chosen for each solution for each ant.
		@type 		medians:	Numpy Array of Integer.
		'''

	def __init__(self, p, clients, maxit, antn, decayr, alpha, beta):
		''' Initializes an instance of the Ant Colony Optimization Problem.
		
			@param	p:	Number of medians.
			@type	p:	Integer.

			@param	clients:	Clients.
			@type 	clients:	List of Client.

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

	def sort_nodes(self, i):
		''' Sort all nodes based on their distance to node @i.

			@param 	i: 	Node to be used as reference.
			@type	i:	Integer.

			@return:	Sorted nodes based on their distance to node @i.
			@type:		List of Client.
			'''

		distances = sorted(list(zip(list(range(self.n)), self.d[i])),
			key=lambda x: x[1])
		del(distances[0])		

		return [self.clients[i[0]] for i in distances]

	def allocate(self, i, ordered_nodes):
		''' Assign each node in @ordered_nodes to node @i, until its capacity is
			reached.

			@param 	i: 	Node to assign nodes to.
			@type 	i:	Integer.

			@param 	ordered_nodes: 	Sorted nodes based on their distance to node
									@i.
			@type 	ordered_nodes:	List of Client.

			@return 	all_nodes: 	Number of allocated nodes.
			@rtype		all_nodes:	Integer.

			@return 	sum_distance:	The summation of the distance between
										each allocated node and node @i.
			@rtype 		sum_distance:	Float.
			'''

		all_nodes = 0
		sum_distance = 0
		used_capacity = 0
		node_i = self.clients[i]

		for node in ordered_nodes:
			used_capacity += node.demand

			if (used_capacity > node_i.capacity):
				break
			else:
				all_nodes += 1
				sum_distance += self.d[i, node.id]
				# print(i, node.id)

		# print('allocate', all_nodes, sum_distance)
		return all_nodes, sum_distance

	def density(self, i):
		''' Calculate the optimistic density of a cluster if a given node @i was
			to be chosen as the median.
			
			@param 	i:	Node to be chosen as the median.
			@type	i:	Integer.

			@return:	Optimistic density of a cluster if a given node @i was
						to be chosen as the median.
			@rtype:		Float.
			'''

		ordered_nodes = self.sort_nodes(i)
		all_nodes, sum_distance = self.allocate(i, ordered_nodes)
		return all_nodes / sum_distance

	def get_nodes_probs(self, chosen):
		''' Get the probabilities to choose Clients as medians.

			@param 	chosen:	Clients already chosen as medians.
			@type	chosen:	List of Integer.

			@return:	Probabilities to choose Clients as medians.
			@rtype:		List of Float.
			'''

		weights = []
		for node in self.clients:
			if (node.id in chosen):
				weights.append(0)
			else:
				p = self.pheromone[node.id] ** self.alpha
				ni = self.density(node.id) ** self.beta
				weight = p * ni
				weights.append(weight)

		w_sum = sum(weights)
		probs = [(weights[i]/w_sum) if i not in chosen else 0 \
			for i in range(self.n)]
		return probs

	def choose_medians(self):
		''' Using the probabilistic equation, choose a set of p nodes to become
			medians among the n candidate nodes.
			'''
		pass


	def build_solution(self):
		''' Build a solution to the problem using the current pheromone
			setting and ants.
			'''
		pass


	def update_pheromone(self):
		'''	Update pheromone vector based on the paths the ants are using to
			build solutions. 
			'''
		pass

	def ant_system(self):
		''' Run the Ant System algorithm.
			'''

		for it in range(self.maxit):
			for ant in range(self.antn):
				self.build_solution()
			
			self.update_pheromone()

		# TODO

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