import nltk, re, copy
from sets import Set
from nltk.corpus import treebank

# Get numsents POS-tagged sentences from the treebank corpus
def get_pos_data(numsents):

    # Extract required number of sentences
    sentences = treebank.tagged_sents()[:numsents]

    # Initialize
    sequences = []
    symbols = Set()
    tag_set = Set()
    
    # Go over each extracted sentence ...
    for sentence in sentences:
        for i in range(len(sentence)):
            word, tag = sentence[i]
            word = word.lower()  # normalize case
            symbols.add(word)    # add this word
            tag_set.add(tag)
            sentence[i] = (word, tag)  # store tagged token
        sequences.append(sentence)

    # Return sequences, the list of tags and all the words that we saw
    return sequences, list(tag_set), list(symbols)

# Train the tranition and emission probabilities
def train():
    print 'Training HMM...'

    # Use the first 3000 sentences from treebank corpus
    labelled_sequences, states, symbols = get_pos_data(3000)
    
    # Define the estimator to be used for probability computation
    estimator = lambda fd, bins: nltk.LidstoneProbDist(fd, 0.1, bins)
    
    # count occurences of starting states, transitions out of each state
    # and output symbols observed in each state
    freq_starts = nltk.FreqDist()
    freq_transitions = nltk.ConditionalFreqDist()
    freq_emissions = nltk.ConditionalFreqDist()
    for sequence in labelled_sequences:
        lasts = None
        for token in sequence:
            state = token[1]
            symbol = token[0]
            if lasts == None:
                freq_starts.inc(state)
            else:
                freq_transitions[lasts].inc(state)
            freq_emissions[state].inc(symbol)
            lasts = state

            # update the state and symbol lists
            if state not in states:
                states.append(state)
            if symbol not in symbols:
                symbols.append(symbol)

    # create probability distributions (with smoothing)
    N = len(states)
    starts = estimator(freq_starts, N)
    transitions = nltk.ConditionalProbDist(freq_transitions, estimator, N)
    emissions = nltk.ConditionalProbDist(freq_emissions, estimator, len(symbols))
                               
    # Return the transition and emissions probabilities along with 
    # the list of all the states and output symbols
    return starts, transitions, emissions, states, symbols