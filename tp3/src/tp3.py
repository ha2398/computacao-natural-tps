#!/usr/bin/env python3

'''
tp3.py: Artificial Neural Networks
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''


import argparse as ap
import numpy as np

# Add comand line arguments
parser = ap.ArgumentParser()

parser.add_argument('input_filename', type=str, help='Name of input file')
parser.add_argument('output_filename', type=str, help='Name of output file')

parser.add_argument('-e', dest='EPOCHS', default = 100, type=int,
	help='Number of epochs to run the program for')
parser.add_argument('-l', dest='HLAYERS', default = 1, type=int,
	help='Number of hidden layers in the network')
parser.add_argument('-n', dest='NEURONS', default = 10, type=int,
	help='Number of neurons on each hidden layer')
parser.add_argument('-b', dest='BATCHSIZE', default = 10, type=int,
	help='Size of the batches fed into the network')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Numpy random seed')
parser.add_argument('-r', dest='LRATE', default=0.1, type=float,
	help='Learning rate')
parser.add_argument('-d', dest='LRDECAY', default=0., type=float,
	help='Learning rate decay')

args = parser.parse_args()

# Set random generator seed
np.random.seed(args.RSEED)

# Keras modules
from keras import optimizers
from keras import initializers
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils


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


def create_network(n_features, n_classes):
	''' Create a new neural network. 

		@param 	n_features:	Number of features in input data.
		@type 	n_features:	Integer.

		@param 	n_classes:	Number of classes in output data.
		@type 	n_classes:	Integer.

		@return:	New neural network.
		@rtype: 	keras.models.Sequential
		'''

	model = Sequential()

	init = 'lecun_uniform'

	# Input layer
	model.add(Dense(args.NEURONS, kernel_initializer=init, input_dim=n_features,
	 activation='relu'))

	# Hidden layers
	for i in range(args.HLAYERS):
		model.add(Dense(args.NEURONS, kernel_initializer=init,
			activation='relu'))

	# Output layer
	model.add(Dense(n_classes, kernel_initializer=init, activation='softmax'))

	# Optimizer
	sgd = optimizers.SGD(lr=args.LRATE, decay=args.LRDECAY)

	model.compile(loss='categorical_crossentropy', optimizer=sgd,
		metrics=['accuracy'])

	return model


def main():

	X, Y = read_input(args.input_filename)

	output = open(args.output_filename, 'w')

	# Encode classes
	encoded_Y = encode_classes(Y)
	categorical_Y = np_utils.to_categorical(encoded_Y)

	num_features = len(X[0])
	num_classes = len(categorical_Y[0])

	# Training and evalutation
	indices = np.arange(len(X))
	cur_K = 1
	for training, test in k_fold_cross_validation(indices, K=3):
		output.write('[+] Fold ' + str(cur_K) + '\n')
		network = create_network(num_features, num_classes)
		mfit = network.fit(X[training], categorical_Y[training],
			epochs=args.EPOCHS, batch_size=args.BATCHSIZE, verbose=0)
		meval = network.evaluate(X[test], categorical_Y[test])

		output.write('acc: ' + str(mfit.history['acc']) + '\n')
		output.write('loss: ' + str(mfit.history['loss']) + '\n')
		output.write('test: ' + str(meval) + '\n')
		output.write('\n')
		cur_K += 1 

	output.close()

main()