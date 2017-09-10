#!/usr/bin/env python3

'''
tp1.py
@author: Hugo Araujo de Sousa [2013007463]
@DCC191
'''

import argparse

# Adds optional command line arguments to the program.
parser = argparse.ArgumentParser()
parser.add_argument('-d', dest='MAX_DEPTH', default=7, type=int,
	help='Maximum depth of the individual trees')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Random number generation seed')
parser.add_argument('-p', dest='POP_SIZE', default=0, type=int,
	help='Population size')

args = parser.parse_args()

# Random numbers generation setup. '''
import random
random.seed(args.RSEED)

import individual as ind


def main():
	a = ind.Individual.full(args.MAX_DEPTH, 5)
	print(a)


main()