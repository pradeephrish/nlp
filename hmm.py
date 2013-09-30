#!/usr/bin/env python

from numpy import zeros, float32
import sys, hmmtrain

class hmm:        
    def __init__(self):
		'''
        priors, transitions, emissions, states, symbols = hmmtrain.train()
        self.priors = priors
        self.transitions = transitions
        self.emissions = emissions
        self.states = states
        self.symbols = symbols
		'''
		
    def exhaustive(self):
		input = 'You look around at professional ballplayers and nobody blinks an eye'
		input = input.lower()    #convert to lower case
		input = input.split()   #tokenize
		viterbi= zeros(shape=(12,len(input)),dtype=float32);  #float32 numpy array for precision,  hardcoded lenth of token for alog, modify later size+2
		print viterbi
		print input
		
		
    ####
    # ADD METHODS HERE
    ####
    


def main():
    # Create an instance
    model = hmm().exhaustive()

	
	

if __name__ == '__main__':
    main()
