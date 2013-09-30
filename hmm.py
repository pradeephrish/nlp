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
		input = 'You look around at professional ballplayers and nobody blinks an eye'+ ' .'
		input = input.lower()    #convert to lower case
		input = input.split()   #tokenize
		#input = input.append('.') #for termination phase    -- added with string
		viterbi= zeros(shape=(len(self.states),len(input)),dtype=float32);  #float32 numpy array for precision, why  first 2
		backpointers= zeros(shape=(len(self.states),len(input)));
		print viterbi
		print input
		sym=input[0]  #take first observation/word
		for i,state in enumerate(self.states):
			viterbi[i,0]= self.priors.logprob(state) + self.emissions[state].logprob(sym) #use priors for start frequency, log scale therfore plus
			backpointers[i,0]=0
			#save backpoint
			#print state

		print viterbi
		print 'backpointers'
		print backpointers
		iterinputs = iter(input)
		for k,word in enumerate(iterinputs):
			for s,state in enumerate(self.states):
				#find maximum from viterbi[s',t-1] and store that s' for a(s',s)
				max=viterbi[0,k-1];
				argMaxSum=viterbi[0,k-1]+ self.transitions[state].logprob(state)
				maxStateId = 0; #since max initialized to zero, this is s'
				argMaxStateId=0;
				for p,stateIn in enumerate(self.states):
					if max < viterbi[p,k-1]:
						max=viterbi[p,k-1]
						maxStateId = p;
					if argMaxSum < viterbi[p,k-1]+ self.transitions[stateIn].logprob(state):
						argMaxSum= viterbi[p,k-1]+ self.transitions[stateIn].logprob(state)
						argMaxStateId=p;
						
				#above function finished, found maximum ,s' stored in maxStateId   ,  Note  viterbi[maxStateId,k-1] is equal to max
				viterbi[s,k]=viterbi[maxStateId,k-1]+ self.transitions[self.states[maxStateId]].logprob(state)+self.emissions[state].logprob(word)#note log scale -> plus
				backpointers[s,k]=argMaxStateId
		#termination step  T (oT = '.') , input/words/observations were appended by . therefore termination should happen at this stage
		'''
		print 'before final step'
		print verterbi
		qf=len(self.states)
		T=len(input)
		'''
		#find max and T (oT = '.')
    ####
    # ADD METHODS HERE
    ####
		print 'terminating'
		print viterbi
		print backpointers
		return backpointers


def main():
    # Create an instance
    model = hmm().exhaustive()
	#print 'everthing went fine, now printing backpointers'
	#print model

	
	

if __name__ == '__main__':
    main()
