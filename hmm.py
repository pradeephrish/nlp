#!/usr/bin/env python

from numpy import zeros, float32
import sys, hmmtrain

class hmm:        
    def __init__(self):
        priors, transitions, emissions, states, symbols = hmmtrain.train()
        self.priors = priors
        self.transitions = transitions
        self.emissions = emissions
        self.states = states
        self.symbols = symbols
		
    def exhaustive():
		
    ####
    # ADD METHODS HERE
    ####
    


def main():
    # Create an instance
    model = hmm()
	

if __name__ == '__main__':
    main()
