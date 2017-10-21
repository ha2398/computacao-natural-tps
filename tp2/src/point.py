#!/usr/bin/env python3

'''
point.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

class Point():
	''' Defines a point in a two dimensional space. '''

	def __init__(self, x, y, c, d):
		''' Initializes a point.

			@param	x: x coordinate of the point.
			@type	x: Float.

			@param	y: y coordinate of the point.
			@type	y: Float.

			@param	c: Point's capacity.
			@type 	c: Float.

			@param	d: Point's demand.
			@type	d: Float
			'''

		self.x = x
		self.y = y
		self.c = c
		self.d = d

	def distance(self, point):
		''' Get euclidean distance between two points.

			@param	point:	Second point.
			@type	point:	Point.

			@return:		Distance between self and point.
			@rtype:			Float.
			'''

		return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5


def build_distance_matrix(points):
	''' Build distance matrix D where Dij indicates the distance between point i
		and j.

		@param	points:	List with all points.
		@type	points:	List of Point.

		@return:		Matrix D of distances.		
		@rtype:			List of list of floats.
		'''

	size = len(points)
	D = []
	for i in range(size):
		D.append([0] * size)

	for i in range(size):
		for j in range(i, size):
			D[i][j] = D[j][i] = points[i].distance(points[j])

	return D