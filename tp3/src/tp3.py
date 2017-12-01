#!/usr/bin/env python3

'''
tp3.py: Artificial Neural Networks
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''


from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils

import argparse as ap
import numpy as np


def parse_arguments():
	''' Add command line arguments to the program.

		@return:	Command line arguments.
		@rtype:		argparse.Namespace.
		'''

	parser = ap.ArgumentParser()

	parser.add_argument('input_filename', type=str, help='Name of input file')
	parser.add_argument('-e', dest='EPOCHS', default = 100, type=int,
		help='Number of epochs to run the program for')
	parser.add_argument('-l', dest='HLAYERS', default = 1, type=int,
		help='Number of hidden layers in the network')
	parser.add_argument('-n', dest='NEURONS', default = 10, type=int,
		help='Number of neurons on each hidden layer')
	parser.add_argument('-b', dest='BATCHSIZE', default = 10, type=int,
		help='Size of the batches fed into the network')
	parser.add_argument('-k', dest='KFOLD', default = 200, type=int,
		help='K fold size to use in cross validation')
	parser.add_argument('-s', dest='RSEED', default=0, type=int,
		help='Numpy random seed')

	args = parser.parse_args()
	return args


def read_input(input_filename):
	''' Read input data and format it into data and target arrays.

		@param 	input_filename: Name of the input file.
		@type 	input_filename: String.

		@return: 	Data and target arrays.
		@rtype:		Numpy array, Numpy array.
		'''

	dataset = np.loadtxt(input_filename, delimiter=';', dtype=object)
	input_dim = len(dataset[0]) - 1
	X = dataset[:,:input_dim].astype(float)
	Y = dataset[:,input_dim]

	return X, Y


def k_fold_cross_validation(X, K, randomise = False):
	''' Generate K (training, validation) pairs from the items in X.

		Each pair is a partition of X, where validation is an iterable.
		of length len(X)/K. So each training iterable is of length
		(K-1)*len(X)/K.

		If randomise is true, a copy of X is shuffled before partitioning,
		otherwise its order is preserved in training and validation.

		@param 	X:	Input data.
		@type 	X:	Numpy Array.

		@param 	K:	Size of each fold.
		@type 	K:	Integer.

		@param 	randomise: 	Indicates if the data should be shuffled.
		@type 	randomise:	Boolean.

		@return:	K (training, validation) pairs from items in X.
		@rtype:		Numpy Array, Numpy Array.
		'''

	if randomise:
		np.random.shuffle(X)
	for k in range(K):
		training = np.array([x for i, x in enumerate(X) if i % K != k])
		validation = np.array([x for i, x in enumerate(X) if i % K == k])
		yield training, validation


def encode_classes(Y):
	''' Encode classes in dataset.

		@param 	Y: 	Target classes list.
		@type 	Y: 	Numpy Array.

		@return:	Encoded list of classes.
		@rtype: 	Numpy Array.
		'''

	class_code = {}
	class_set = set(Y)
	encoded = []

	for c in Y:
		if c not in class_code:
			code = len(class_code)
			class_code[c] = code
		else:
			code = class_code[c]

		encoded.append(code)

	return np.array(encoded)


def create_network(n_features, n_classes, n_layers, n_neurons):
	''' Create a new neural network. 

		@param 	n_features:	Number of features in input data.
		@type 	n_features:	Integer.

		@param 	n_classes:	Number of classes in output data.
		@type 	n_classes:	Integer.

		@param 	n_layers:	Number of hidden layers on the network.
		@type 	n_layers:	Integer.

		@param 	n_neurons:	Number of neurons on each hidden layer.
		@type 	n_neurons:	Integer.

		@return:	New neural network.
		@rtype: 	keras.models.Sequential
		'''

	model = Sequential()

	model.add(Dense(n_neurons, input_dim=n_features, activation='relu'))

	for i in range(n_layers):
		model.add(Dense(n_neurons, activation='relu'))

	model.add(Dense(n_classes, activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='sgd',
		metrics=['accuracy'])

	return model


def main():

	args = parse_arguments()
	np.random.seed(args.RSEED)
	X, Y = read_input(args.input_filename)

	encoded_Y = encode_classes(Y)
	categorical_Y = np_utils.to_categorical(encoded_Y)

	num_features = len(X[0])
	num_classes = len(categorical_Y[0])

	network = create_network(num_features, num_classes, args.HLAYERS,
		args.NEURONS)

	indices = np.arange(len(X))
	for training, test in k_fold_cross_validation(indices, K=args.KFOLD):
		mfit = network.fit(X[training], categorical_Y[training],
			epochs=args.EPOCHS, batch_size=args.BATCHSIZE)
		meval = network.evaluate(X[test], categorical_Y[test])
		print(meval)


main()