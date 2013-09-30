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
		k=1
		for word in iterinputs:
			i = 0
			for state in self.states:
				#find maximum from viterbi[s',t-1] and store that s' for a(s',s)
				max=viterbi[0,k-1];
				argMaxSum=viterbi[0,k-1]+ self.transitions[state].logprob(state)
				maxStateId = 0; #since max initialized to zero, this is s'
				argMaxStateId=0;
				p = 0
				for stateIn in self.states
					if max < viterbi[p,k-1]
						max=viterbi[p,k-1]
						maxStateId = p;
					if argMaxSum < viterbi[p,k-1]+ self.transitions[stateIn].logprob(state)
						argMaxSum= viterbi[p,k-1]+ self.transitions[stateIn].logprob(state)
						argMaxStateId=p;
					p=p+1
						
				#above function finished, found maximum ,s' stored in maxStateId   ,  Note  viterbi[maxStateId,k-1] is equal to max
				viterbi[i,k]=viterbi[maxStateId,k-1]+ self.transitions[self.states[maxStateId]].logprob(state)+self.emissions[state].logprob(word)#note log scale -> plus 
				backpointers[i,k]=
		        i = i+1
		k = k+1
    ####
    # ADD METHODS HERE
    ####
    


def main():
    # Create an instance
    model = hmm().exhaustive()

	
	

if __name__ == '__main__':
    main()
