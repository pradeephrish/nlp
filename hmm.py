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
		
		
    def exhaustive(self):
		input = 'You look around at professional ballplayers and nobody blinks an eye'
		input = input.lower()    #convert to lower case
		input = input.split()   #tokenize
		viterbi= zeros(shape=(len(self.states)+2,len(input)),dtype=float32);  #float32 numpy array for precision
		backpointers= zeros(shape=(len(self.states)+2,len(input)));
		print viterbi
		print input
		sym=input[0]  #take first observation/word
		i=0
		for state in self.states:
			viterbi[i,0]= self.priors.logprob(state) + self.emissions[state].logprob(sym) #use priors for start frequency, log scale therfore plus
			backpointers[i,0]=0
			i=i+1
			#save backpoint
			#print state
		print viterbi
		print 'backpointers'
		print backpointers
		iterinputs = iter(input)
		next(iterinputs)      #skip first element
		for word in iterinputs:
			
		
		
    ####
    # ADD METHODS HERE
    ####
    


def main():
    # Create an instance
    model = hmm().exhaustive()

	
	

if __name__ == '__main__':
    main()
