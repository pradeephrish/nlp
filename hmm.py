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
		print input
		
    ####
    # ADD METHODS HERE
    ####
    


def main():
    # Create an instance
    model = hmm().exhaustive()

	
	

if __name__ == '__main__':
    main()
