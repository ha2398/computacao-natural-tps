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

		@attribute 	pheromone: 	Pheromone vector.
		@type 		pheromone:	Numpy Array of Float.

		@attribute 	pher_max:	Maximum value for pheromone.
		@type 		pher_max:	Float.

		@attribute 	pher_min:	Minimum value for pheromone.
		@type 		pher_min:	Float.

		@attribute 	pher_init:	Initial value for pheromone.
		@type 		pher_init:	Float.

		@attribute 	stag_ctrl_value:	Stagnation control value.
		@type 		stag_ctrl_value:	Float.

		@attribute 	best_global: 	Best solution cost found.
		@type 		best_global:	Float.

		@attribute 	worst_global: 	Worst solution cost found.
		@type 		worst_global:	Float.

		@attribute 	solution: 	Best solution, i.e., clients chosen as medians
								at the end of the program.
		@type		solution:	List of Integer.
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
		self.n = len(clients)
		self.d = self.build_distance_matrix()

		# x_ij = 1 if node i is allocated to median j, 0 otherwise
		self.x = np.zeros((self.n, self.n))

		self.pher_max = 0.999
		self.pher_min = 0.001
		self.pher_init = 0.5

		self.restart_pheromone()
		self.best_global = np.inf
		self.worst_global = -1 * np.inf

		self.stag_ctrl_value = self.p * self.pher_max + (self.n - self.p) * \
			self.pher_min

		self.solution = []

	def restart_pheromone(self):
		''' Restart pheromone trails. '''

		self.pheromone = np.full(self.n, self.pher_init)

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
		
		clients = list(range(self.n))
		medians = []
		while len(medians) != self.p:
			probs = self.get_nodes_probs(medians)
			medians.append(np.random.choice(clients, p=probs))

		return medians

	def get_nearest_median_dist(self, client, medians):
		''' Get the distance to nearest median to @client.

			@param 	client:	Id of client referenced.
			@type	client:	Integer.

			@param 	medians:	Clients chosen as medians.
			@type	medians:	List of Integer.

			@return:	Distance to nearest median to @client.
			@rtype:		Integer.
			'''

		distances = [(i, self.d[client, i]) for i in range(self.n) \
			if i in medians]
		distances = sorted(distances, key=lambda x: x[1])
		return distances[0][1]

	def sort_clients(self, medians):
		''' Generate a list with all the n clients in increasing order of
			distance to their corresponding nearest median.

			@param 	medians:	Clients chosen as medians.
			@type	medians:	List of Integer.

			@return:	List of clients in increasing order of distance to their
						corresponding nearest median.
			@rtype:		List of Client.
			'''

		clients = [(self.clients[i], self.get_nearest_median_dist(i, medians)) \
			for i in range(self.n)]
		clients = sorted(clients, key=lambda x: x[1])
		return [x[0] for x in clients]

	def sort_medians(self, client, medians):
		''' Generate a list with all the p medians in increasing order of
			distance to the current client.

			@param 	client:	Current client.
			@type	client:	Client.

			@param 	medians:	Clients chosen as medians.
			@type 	medians:	List of Integer.

			@return:	List with all the p medians in increasing order of
						distance to the current client.
			@type:		List of Integer.
			'''

		p_medians = sorted([(i, self.d[client.id, i]) for i in medians],
			key=lambda x: x[1])
		return [x[0] for x in p_medians]

	def GAP(self, medians):
		''' Generalized Assignment Problem heuristic.
			
			@param 	medians: 	Clients chosen to be medians.
			@type	medians:	List of Integer.
			'''

		self.x = np.zeros((self.n, self.n))
		ordered_clients = self.sort_clients(medians)

		for i in range(self.n):
			ordered_medians = self.sort_medians(ordered_clients[i], medians)

			for j in range(self.p):
				m = self.clients[ordered_medians[j]]
				c = ordered_clients[i]
				if (m.capacity - c.demand >= 0):
					self.x[c.id, m.id] = 1

	def build_solution(self):
		''' Build a solution to the problem using the current pheromone
			setting and ants.

			@return:	Medians used in the solution.
			@rtype:		List of Integer.
			'''
		
		medians = self.choose_medians()
		self.GAP(medians)
		return medians

	def update_pheromone(self, medians, cost):
		'''	Update pheromone vector based on the paths the ants are using to
			build solutions. 
			'''
		
		norm_cost = 1 + ((cost - self.best_global)*(0 - 1))/(self.worst_global \
			- self.best_global)
		delta_p = (1 / norm_cost)

		for i in range(self.n):
			self.pheromone[i] = self.decayr * self.pheromone[i]

			if (i in medians):
				self.pheromone[i] += delta_p

		np.clip(self.pheromone, 0.001, 0.999, out=self.pheromone)

		if (abs(sum(self.pheromone) - self.stag_ctrl_value) < 0.1):
			self.restart_pheromone()

	def ant_system(self):
		''' Run the Ant System algorithm.
			'''

		for it in range(self.maxit):
			print("Iteration", it+1, ":")
			best_local = np.inf
			updt_phero = False

			for ant in range(self.antn):
				medians = self.build_solution()
				cost = self.evaluate_solution()

				print("\tAnt:", (ant+1), "medians:", medians, "cost:", cost)

				if (cost < best_local):
					best_local = cost
					best_medians = medians
					updt_phero = True

				if (cost < self.best_global):
					self.best_global = cost
					self.solution = medians

				if (cost > self.worst_global):
					self.worst_global = cost

			if (updt_phero):
				self.update_pheromone(best_medians, best_local)

	def build_distance_matrix(self):
		''' Build distance matrix D where Dij indicates the distance between
			client i and j.

			@return:		Matrix D of distances.		
			@rtype:			Numpy Array of Numpy Array of Float.
			'''

		D = np.zeros((self.n, self.n))

		for i in range(self.n):
			for j in range(i, self.n):
				D[i, j] = D[j, i] = self.clients[i].distance(self.clients[j])

		return D