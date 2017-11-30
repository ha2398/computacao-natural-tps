#!/usr/bin/env python3

'''
tp3.py: Artificial Neural Networks
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''


from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

import argparse as ap
import numpy as np
import pandas as pan

# Global variables
parser = ap.ArgumentParser()

parser.add_argument('input_filename', type=str, help='Name of input file')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Numpy random seed')

args = parser.parse_args()
np.random.seed(args.RSEED)

class_code = {}
code_class = {}


def read_input(input_filename):
	''' Read input data and format it into data and target arrays.

		@param 	input_filename: Name of the input file.
		@type 	input_filename: String.

		@return: 	Data and target arrays.
		@rtype:		Numpy array, Numpy array.
		'''

	dataframe = pan.read_csv(input_filename, header=None, sep=';')
	dataset = dataframe.values
	input_dim = len(dataset[0]) - 1
	X = dataset[:,:input_dim].astype(float)
	Y = dataset[:,input_dim]

	return X, Y


def main():

	global input_dim

	X, Y = read_input(args.input_filename)

	encoder = LabelEncoder()
	encoder.fit(Y)
	encoded_Y = encoder.transform(Y)
	categorical_Y = np_utils.to_categorical(encoded_Y)

	num_features = len(X[0])
	num_classes = len(set(encoded_Y))

	model = Sequential()
	model.add(Dense(64, input_dim=num_features, activation='relu'))
	model.add(Dense(64, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam',
		metrics=['accuracy'])

	model.fit(X, categorical_Y, epochs=200, batch_size=100)


main()