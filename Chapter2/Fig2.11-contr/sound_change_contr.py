#!/usr/bin/env python3

import random
import sys
import matplotlib.pyplot as plt
import numpy as np




'''
1. ALPHABET and LEXICON

This part defines the alphabet of the language, and maps symbols to indexes.

The vowel dictionary maps 15 different symbols onto different indexes.
The consonant dictionary maps 26 different symbols onto different indexes.
'''

vowels = {'i': 0, 'e': 1, 'a': 2, 'o': 3, 'u': 4, 'ou':5, 'ei':6, 'ea':7, 'ee':8, 'oo':9, 'ai':10, 'oa':11,
          'oi':12, 'io':13, 'ie':14}


consonants = {'m': 0, 'p':1, 'b':2, 'f': 3, 'v': 4, 'd': 5, 't': 6, 'l': 7, 'n': 8, 'r': 9, 's': 10, 'k': 11,
              'y': 12, 'g': 13, 'j':14, 'h': 15, 'c':16, ' ':17, 'th':18, 'sh':19, 'wh':20, 'ch':21, 'tw':22,
              'x':23, 'w':24, 'z':25}

'''
With this dictionary, we can represent each word as an integer tuple. Words are initially read from a text file
in the form of 3-dimensional tuples of the type (onset, nucleus, coda). For instance the word "dog" will be 
processed in the form of a 3-dimensional tuple ('d', 'o', 'g'). Then, we can use the two dictionaries to transform 
each word into a integer vector, through a helper function, for computation purposes. The word "dog" will be 
transformed in the tuple (5, 3, 13).
'''

dog = ('d', 'o', 'g')

def vectorize(word):
    onset, nucleus, coda = word
    return consonants[onset], vowels[nucleus], consonants[coda]

print(vectorize(dog))


'''
The lexicon is a list of words (tuples), and is stored as a global variable, since we need to modify it as sound change
occurs. A wordlist containing the words "dog", "cat", and "pig" will be represented by the following variable:
'''

wordlist = [('d', 'o', 'g'), ('c', 'a', 't'), ('p', 'i', 'g')]

'''
Since we want to keep track of the number of symbols and the possible environments, we also store three sets that
contain the onsets, nuclei and codas available in the lexicon in its current state. These three sets are all 
global variables.
'''

def get_onset(wordlist):
    return {word[0] for word in wordlist}

def get_nucleus(wordlist):
    return {word[1] for word in wordlist}

def get_coda(wordlist):
    return {word[2] for word in wordlist}


onset, nucleus, coda = get_onset(wordlist), get_nucleus(wordlist), get_coda(wordlist)

print(onset)
print(nucleus)
print(coda)


'''
For illustratory purposes, we need a reverse-dictionary, which can be used to retrieve the symbols given their index,
and a helper function to retrieve the word (in string format) given its integer vector representation:
'''

rev_vowels = {code: letter for letter, code in vowels.items()}
rev_consonants = {code: letter for letter, code in consonants.items()}


dog = (5, 3, 13)

def vectorize_inverse(word):
    onset, nucleus, coda = word
    return rev_consonants[onset] + rev_vowels[nucleus] + rev_consonants[coda]

print(vectorize_inverse(dog))


'''
Another helper function that we need is a function that returns the average Levenshtein distance within a wordlist:
'''

def average(wordlist):
    av_length = []
    for index, word in enumerate(wordlist):
        for word2 in wordlist[index+1:]:
            lev = 0
            for i, letter in enumerate(word):
                if word2[i] != letter:
                    lev += 1
            av_length.append(lev)
    return sum(av_length)/len(av_length)


print(average(wordlist))


'''
2. SOUND CHANGE FUNCTIONS

This part defines the sound change functions. These functions modify the lexicon by applying sound changes.
The first function represents a sound change that targets the onset of the word.
'''

def change_onset():
    #call the lexicon list and the onset set
    global lexicon, onset
    #prepare a new empty list, that will be filled with the form of the words after the sound change applies
    new_lexicon = []
    #pick an onset at random and name it target. This is the target of the sound change
    target = random.choice(list(onset))
    #pick an onset at random and name it outcome. This is the outcome of the sound change
    outcome = random.choice(list(rev_consonants))
    #select a random subset of nuclei as the conditioning environment
    environment = random.sample(nucleus, random.randint(0, len(nucleus) - 1))
    #apply the change to the lexicon
    for word in lexicon:
        #check words where target is the onset
        if word[0] == target:
            #determine whether the nucleus is in the conditioning environment
            if word[1] in environment:
                #if the nucleus is in the conditioning environment, then change target into outcome
                new_lexicon.append((outcome, word[1], word[2]))
            else:
                #if not, the change does not apply
                new_lexicon.append(word)
        else:
            #if the word does not start with target, the change does not apply
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_consonants[target] + '/ becomes /' + rev_consonants[outcome] + '/ in onset before ['
          + ' '.join([rev_vowels[index] for index in environment]) + ']')
    #Update lexicon and onsets
    lexicon = new_lexicon
    onset = get_onset(lexicon)


'''
The following two functions will apply a change to the nucleus. The only difference between the two is whether
the conditioning environment is the onset or the coda.
'''

def change_nucleus():
    #call the lexicon list and the nucleus set
    global lexicon, nucleus
    #prepare a new empty list, that will be filled with the form of the words after the sound change applies
    new_lexicon = []
    #pick a nucleus at random and name it target. This is the target of the sound change
    target = random.choice(list(nucleus))
    #pick a nucleus at random and name it outcome. This is the outcome of the sound change
    outcome = random.choice(list(rev_vowels))
    #select a random subset of onsets as the conditioning environment
    environment = random.sample(onset, random.randint(0, len(onset) - 1))
    #apply the change to the lexicon
    for word in lexicon:
        #check words where target is the nucleus
        if word[1] == target:
            #determine whether the onset is in the conditioning environment
            if word[0] in environment:
                #if the onset is in the conditioning environment, then change target into outcome
                new_lexicon.append((word[0], outcome, word[2]))
            else:
                #if not, the change does not apply
                new_lexicon.append(word)
        else:
            #if the word does not have target, the change does not apply
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_vowels[target] + '/ becomes /' + rev_vowels[outcome] + '/ after ['
          + ' '.join([rev_consonants[index] for index in environment]) + ']')
    #Update lexicon and nuclei
    lexicon = new_lexicon
    nucleus = get_nucleus(lexicon)

def change_nucleus2():
    #call the lexicon list and the nucleus set
    global lexicon, nucleus
    #prepare a new empty list, that will be filled with the form of the words after the sound change applies
    new_lexicon = []
    #pick a nucleus at random and name it target. This is the target of the sound change
    target = random.choice(list(nucleus))
    #pick a nucleus at random and name it outcome. This is the outcome of the sound change
    outcome = random.choice(list(rev_vowels))
    #select a random subset of codas as the conditioning environment
    environment = random.sample(coda, random.randint(0, len(coda) - 1))
    #apply the change to the lexicon
    for word in lexicon:
        #check words where target is the nucleus
        if word[1] == target:
            #determine whether the coda is in the conditioning environment
            if word[2] in environment:
                #if the coda is in the conditioning environment, then change target into outcome
                new_lexicon.append((word[0], outcome, word[2]))
            else:
                #if not, the change does not apply
                new_lexicon.append(word)
        else:
            #if the word does not have target, the change does not apply
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_vowels[target] + '/ becomes /' + rev_vowels[outcome] + '/ before ['
          + ' '.join([rev_consonants[index] for index in environment]) + ']')
    #Update lexicon and nuclei
    lexicon = new_lexicon
    nucleus = get_nucleus(lexicon)


'''
Finally, this function changes the coda consonant.
'''


def change_coda():
    #call the lexicon list and the coda set
    global lexicon, coda
    #prepare a new empty list, that will be filled with the form of the words after the sound change applies
    new_lexicon = []
    #pick a coda at random and name it target. This is the target of the sound change
    target = random.choice(list(coda))
    #pick a coda at random and name it outcome. This is the outcome of the sound change
    outcome = random.choice(list(rev_consonants))
    #select a random subset of nuclei as the conditioning environment
    environment = random.sample(nucleus, random.randint(0, len(nucleus) - 1))
    #apply the change to the lexicon
    for word in lexicon:
        #check words where target is the coda
        if word[2] == target:
            #determine whether the nucleus is in the conditioning environment
            if word[1] in environment:
                #if the nucleus is in the conditioning environment, then change target into outcome
                new_lexicon.append((word[0], word[1], outcome))
            else:
                #if not, the change does not apply
                new_lexicon.append(word)
        else:
            #if the word does not end with target, the change does not apply
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_consonants[target] + '/ becomes /' + rev_consonants[outcome] + '/ in coda after ['
          + ' '.join([rev_vowels[index] for index in environment]) + ']')
    #Update lexicon and onsets
    lexicon = new_lexicon
    coda = get_coda(lexicon)

'''
Now, we add the two contraction functions:'''

def contraction_onset():
    #call the lexicon list and the onset and nucleus sets
    global lexicon, onset, nucleus
    new_lexicon = []
    #we select a CV sequence as the target of the contraction
    target_C, target_V = random.choice(list(onset)), random.choice(list(nucleus))
    #this selects an outcome among those which are not available in the language
    possible_outcome = [key for key in rev_consonants if key not in onset]
    if possible_outcome:
        outcome = random.choice(possible_outcome)
    #if all the possible onsets are already represented, pick one at random
    else:
        outcome = random.choice(list(onset))
    #this is the vowel added after the new onset
    filler = random.choice(list(nucleus))
    for word in lexicon:
        if (word[0], word[1]) == (target_C, target_V):
            new_lexicon.append((outcome, filler, word[2]))
        else:
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('Contraction of /' + rev_consonants[target_C] + rev_vowels[target_V] + '/ in /' + rev_consonants[outcome] + rev_vowels[filler] + '/ in onsets')
    #Update lexicon and onsets
    lexicon = new_lexicon
    onset, nucleus = get_onset(lexicon), get_nucleus(lexicon)


def contraction_coda():
    #call the lexicon list and the onset and nucleus sets
    global lexicon, nucleus, coda
    new_lexicon = []
    #we select a VC sequence as the target of the contraction
    target_V, target_C = random.choice(list(nucleus)), random.choice(list(coda))
    #this selects an outcome among those which are not available in the language
    possible_outcome = [key for key in rev_consonants if key not in coda]
    if possible_outcome:
        outcome = random.choice(possible_outcome)
    #if all the possible onsets are already represented, pick one at random
    else:
        outcome = random.choice(list(coda))
    #this is the vowel added before the new coda
    filler = random.choice(list(nucleus))
    for word in lexicon:
        if (word[1], word[2]) == (target_V, target_C):
            new_lexicon.append((word[0], filler, outcome))
        else:
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('Contraction of /' + rev_vowels[target_V]+rev_consonants[target_C] + '/ in /' + rev_vowels[filler] + rev_consonants[outcome] + '/ in codas')
    #Update lexicon and onsets
    lexicon = new_lexicon
    nucleus, coda = get_nucleus(lexicon), get_coda(lexicon)



'''
3. THE SOUND CHANGE SIMULATIONS

The following function initiates the sound change simulations and prints the graphs presented in the chapter.
The functions takes three arguments: the name of the file containing the wordlist, the number of changes, and the
number of simulations.
'''


def main(file, n_changes, iterations):
    for i in range(int(iterations)):
        print('#######Language Change is happening!')
        global onset, nucleus, coda, lexicon
        #the initial lexicon is read from a text file. Onsets, nuclei and codas are separated by a '-'
        initial_lexicon = [element.strip('\n').split('-') for element in open(file)]
        #this line loads the lexicon in the format described above: a list of integer tuples
        lexicon = [(consonants[word[0]], vowels[word[1]], consonants[word[2]]) for word in initial_lexicon]
        #this line gets the onset, nucleus, and coda sets
        onset, nucleus, coda = get_onset(lexicon), get_nucleus(lexicon), get_coda(lexicon)
        #this line will be used to define the sound change functions used in the simulation and their weight
        #with this setting, each function is equally weighted
        functions = [change_onset, change_nucleus, change_nucleus2, change_coda, contraction_onset, contraction_coda]
        #we initialize lists that will keep track of the number of the iteration, the number of the phonemes,
        #and the average distance
        x_axis = [0]
        phonemes = [len(onset.union(coda)) + len(nucleus)]
        av_length = [average(lexicon)]
        for n in range(int(n_changes)):
            #this line selects a sound change function at random and applies it
            random.choice(functions)()
            #This is needed to make the plot lighter. For the toy example in Figure 2.2, '500' has been reduced to '1'
            if n % 500 == 0:
                #we update the lists that keep track of the number of the iteration, the number of the phonemes, and the
                #average distance
                x_axis.append(n+1)
                phonemes.append(len(onset.union(coda)) + len(nucleus))
                av_length.append(average(lexicon))
                #this loop prints the shape of the lexicon at the beginning of the simulation and after the
                #sound changes applied
                for index, word in enumerate(lexicon):
                    print(''.join(initial_lexicon[index]) + '->' + ''.join(rev_consonants[word[0]] + rev_vowels[word[1]] + rev_consonants[word[2]]))
        print('#######Language Change is finished!')
        print('###################################!')
        #After the simulation has ended, we plot the change in the number of phonemes and in the average distance
        #during the simulation
        #plot phoneme size
        plt.subplot(1, 2, 1)
        plt.plot(x_axis, phonemes)
        #plt.xticks(np.arange(1, 4, step=1)) #This is for the toy example in Figure 2.2
        #plt.yticks(np.arange(36, 39, step=1)) #This is for the toy example in Figure 2.2
        plt.title('Number of Phonemes')
        plt.xlabel('Iterations')
        plt.ylabel('Counts')
        #plot av_length
        plt.subplot(1, 2, 2)
        plt.plot(x_axis, av_length)
        #plt.xticks(np.arange(1, 4, step=1))  #This is for the toy example in Figure 2.2
        plt.title('Average Levenshtein Distance')
        plt.xlabel('Iterations')
        plt.ylabel('Counts')
    plt.show()


if __name__ == "__main__":
    print('###################################!')
    main(sys.argv[1], sys.argv[2], sys.argv[3])


