#!/usr/bin/env python

from numpy import zeros, float32, int32, argmax, max
import hmmtrain
import itertools as itertools


class hmm:
    def __init__(self):
        priors, transitions, emissions, states, symbols = hmmtrain.train()
        self.priors = priors
        self.transitions = transitions
        self.emissions = emissions
        self.states = states
        self.symbols = symbols

    def exhaustive(self,input):
        print('Exhaustive method')
        input=input.lower()
        input=input.split()
        #short listing tags
        print('previous length'),

        tagWords = []
        for word in input:
            tagCopy = self.states[:] #copying list
            removeIndices=[]
            for k,state in enumerate(self.states):
                prob=self.emissions[state].prob(word) #note for comparision not using log
                if(prob < 1e-4):
                    removeIndices.append(k)
            for  i in removeIndices:
                tagCopy.remove(self.states[i])
            tagWords.append(tagCopy)


        #print
        print('after shortlisting')
        print(tagWords)
        #get all combinations of tags
        allCombinations = itertools.product(*tagWords) #one shot using python ,reference: http://stackoverflow.com/questions/798854/all-combinations-of-a-list-of-lists
        newList = list(allCombinations)
        print('printing all combinations')
        #print(allCombinations)
        #for combination in allCombinations:
        #    print combination
        scores=[] #stores probability score for sequence i , starts from zero
        for combination in newList:
            probabilityScoreCombination=0
            for i,state in enumerate(combination):   #note number of states in each combination are same as number of observations
                if(i==0):#use priori for start index
                    probabilityScoreCombination=probabilityScoreCombination+self.priors.logprob(state)+self.emissions[state].logprob(input[i])
                else:
                    probabilityScoreCombination=probabilityScoreCombination+self.emissions[state].logprob(input[i])
            scores.append(probabilityScoreCombination)

        #find maximum probability combination
        maxIndex=argmax(scores)
        #print maximum likely sequence and
        print('Probability :'),
        print(scores[maxIndex])
        print('Maximum likely tag sequence :'),
        print(newList[maxIndex])
        #return allCombinations.pop(maxIndex)

    def forward(self,input): #assumigng end state will  .  (dot)
        #input = 'You look around at professional ballplayers and nobody blinks an eye'+ ' .'
        input = input.lower()    #convert to lower case
        input = input.split()   #tokenize
        #input = input.append('.') #for termination phase    -- added with string
        forward = zeros(shape=(len(self.states), len(input)),dtype=float32);
        sym = input[0]  #take first observation/word
        for i, state in enumerate(self.states):
            forward[i, 0] = self.priors.logprob(state) + self.emissions[state].logprob(sym) #use priors for start frequency, log scale therfore plus


        iterinputs = iter(input)
        for k, word in enumerate(iterinputs):
            for s, state in enumerate(self.states):
                #find sum of viterbi[s',t-1] and store that s' for a(s',s)
                sum=0
                for p,stateIn in enumerate(self.states):
                        sum =sum + forward[p, k - 1] + self.transitions[stateIn].logprob(state);

                #above function finished, calculated sum in sum
                forward[s, k] =  sum + self.emissions[state].logprob(word)#note log scale -> plus

        #found likelihood sequence print sequence
        #find tags
        print forward
        tags = []
        for row in forward:
            ###iterate over states and find maximum
            m = max(row)
            print row,
            maxIndex=0
            for i, j in enumerate(row):
                if j == m:
                    maxIndex=i
            print maxIndex
            tags.append(self.states[maxIndex])

        for word,i in zip(input,tags):
                print word+'/'+i+' ',
        print '***'



    def tagViterbi(self,fileName):
        f=open(fileName,'rU')
        for line in f:
            tags=[]
            path=self.decode(line)
            words= line.split()
            index =path[len(self.states)-1,len(words)] #line was appended by . for final state, therefore no minus 1
            tags.append(self.states[index])
            size=len(words)-1
            for i in (range(size,0,-1)):
                tags.append(self.states[path[index,i]])
                index=path[index,i]


            for word,i in zip(words,reversed(tags)):
                print word+'/'+i+' ',
            print '***'

    def decode(self, input):  #assuming end state will be . dot .
        #input =input+' .'
        #input = 'You look around at professional ballplayers and nobody blinks an eye'+ ' .'
        input = input.lower()    #convert to lower case
        input = input.split()   #tokenize
        #input = input.append('.') #for termination phase    -- added with string
        viterbi = zeros(shape=(len(self.states), len(input)),
                        dtype=float32);  #float32 numpy array for precision, why  first 2
        backpointers = zeros(shape=(len(self.states), len(input)),dtype=int32);
        #print viterbi
        #print input
        sym = input[0]  #take first observation/word
        for i, state in enumerate(self.states):
            viterbi[i, 0] = self.priors.logprob(state) + self.emissions[state].logprob(
                sym) #use priors for start frequency, log scale therfore plus
            backpointers[i, 0] = 0
        #save backpoint
        #print state

        #print viterbi
        #print 'backpointers'
        #print backpointers
        iterinputs = iter(input)
        for k, word in enumerate(iterinputs):
            for s, state in enumerate(self.states):
                #find maximum from viterbi[s',t-1] and store that s' for a(s',s)
                max = viterbi[0, k - 1];
                argMaxSum = viterbi[0, k - 1] + self.transitions[state].logprob(state)
                maxStateId = 0; #since max initialized to zero, this is s'
                argMaxStateId = 0;
                for p, stateIn in enumerate(self.states):
                    if max < viterbi[p, k - 1]:
                        max = viterbi[p, k - 1]
                        maxStateId = p;
                    if argMaxSum < viterbi[p, k - 1] + self.transitions[stateIn].logprob(state):
                        argMaxSum = viterbi[p, k - 1] + self.transitions[stateIn].logprob(state)
                        argMaxStateId = p;

                #above function finished, found maximum ,s' stored in maxStateId   ,  Note  viterbi[maxStateId,k-1] is equal to max
                viterbi[s, k] = viterbi[maxStateId, k - 1] + self.transitions[self.states[maxStateId]].logprob(state) + \
                                self.emissions[state].logprob(word)#note log scale -> plus
                backpointers[s, k] = argMaxStateId
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
        #print 'terminating'
        #print viterbi
        #print backpointers
        return backpointers


def main():
    # Create an instance
    input = 'You look around at professional ballplayers and nobody blinks an eye .'
    #model = hmm().decode(input)

    #Following For Question 2- d
    #model = hmm().tagViterbi('sentences.txt')

    #For question 1-b)
    input = 'You look around at professional ballplayers and nobody blinks an eye .'
    model = hmm().exhaustive(input)
    print model

#print 'everthing went fine, now printing backpointers'
#print model




if __name__ == '__main__':
    main()
