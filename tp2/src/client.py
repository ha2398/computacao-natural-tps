#!/usr/bin/env python3

'''
client.py: Client class
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

class Client():
	''' Defines a client in a two dimensional space.

		Attributes:

		@attribute	x: x coordinate of the client.
		@type		x: Float.

		@attribute	y: y coordinate of the client.
		@type		y: Float.

		@attribute	capacity: 	Client's capacity.
		@type 		cpacity: 	Float.

		@attribute	demand: Client's demand.
		@type		demand: Float
		'''

	def __init__(self, id, x, y, c, d):
		''' Initializes a client.

			@param 	id:	Client identifier.
			@type	id:	Integer.

			@param	x: 	x coordinate of the client.
			@type	x: 	Float.

			@param	y: 	y coordinate of the client.
			@type	y: 	Float.

			@param	c: 	Client's capacity.
			@type 	c: 	Float.

			@param	d: 	Client's demand.
			@type	d: 	Float.
			'''

		self.id = int(id)
		self.x = float(x)
		self.y = float(y)
		self.capacity = float(c)
		self.demand = float(d)

		self.used_cpct = 0

	def __str__(self):
		''' Return a string representation of a client.

			@return:	String representation of a client.
			@rtype:		String.
			'''

		return 	str(self.id) + ' ' + str(self.x) + ' ' + str(self.y) + ' ' + \
				str(self.capacity) + ' ' + str(self.demand)

	def distance(self, client):
		''' Get euclidean distance between two clients.

			@param	client:	Second client.
			@type	client:	Client.

			@return:	Distance between self and client.
			@rtype:		Float.
			'''

		return ((self.x - client.x) ** 2 + (self.y - client.y) ** 2) ** 0.5