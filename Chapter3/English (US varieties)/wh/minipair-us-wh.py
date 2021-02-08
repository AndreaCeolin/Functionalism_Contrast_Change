#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict


'''
This script is used to retrieve the number of minimal pairs associated to each phoneme
'''

def minimal_pairs(wordlist, phoneme):
    '''
    :param wordlist: this is the file containing the corpus
    :param phoneme: this is the phoneme of which we want to retrieve the minimal pairs
    :return: None
    '''
    #this classifies words by length classes (length:list of words) and facilitates the minimal pair algorithm
    word_dic = defaultdict(list)
    for word in wordlist:
        word_dic[len(word)].append(word)
    #this keeps tracks of the minimal pairs
    words = defaultdict(list)
    for word_class in word_dic:
        for index, word in enumerate(word_dic[word_class]):
            for word2 in word_dic[word_class][index+1:]:
                #retrieve all the differences between two words of the same length
                pairs = set([(letter1, letter2) for letter1, letter2 in zip(word,word2) if letter1 != letter2])
                #if the difference is exactly in one phoneme, store it as a minimal pair
                if len(pairs) == 1:
                    pair = pairs.pop()
                    words[pair].append((word, word2))
    #since so far we stored minimal pair of the form x-y and also y-x, we need to merge them under the same key
    dict = defaultdict(list)
    for pair in words:
        if (pair[1], pair[0]) in dict:
            dict[(pair[1], pair[0])].extend(words[pair])
        else:
            dict[pair] = words[pair]
    #print number and words associated to the minimal pairs of the phoneme you are interested in
    for pair in dict:
        if phoneme in pair:
            print(pair, len(dict[pair]), dict[pair])


'''
Since the CMU dictionary encodes the phoneme we are interested in as two separate symbols 'HH' and 'W', we need
a function to merge them
'''

def merge_w(word):
    return word.replace('HH W ', 'HHW ')




'''
In the CMU dictionary, pronunciations with the form 'HH W' are listed as the last entry among all possible ones.
For this reason, we need to go through all the alternative pronunciations, and stores only the last one
'''

wordlist =[]

for line in open('american_corpus.txt'):
    #If there is an alternative pronunciation (the variety ends with the symbol ')'), the alternative pronunciaton
    #replaces the original one. This applies recursively: if there are 3 or 4 different pronunciations, only the last
    #one is retrieved, since that is the one that contains the 'HH W' symbols.
    if line.split()[0][-1] == ')':
        wordlist.pop()
        #we apply the function to retrieve the HHW symbol, and we exclude the first (the word)
        #and last (the frequency count) element of the line
        wordlist.append(merge_w(line).split()[1:-1])
    else:
        wordlist.append(merge_w(line).split()[1:-1])


'''
Double check that the size of the list is the expected one
'''
print(len(wordlist))


'''
Print the minimal pairs along with their count
'''
minimal_pairs(wordlist, 'HHW')


'''
Print phoneme frequencies
'''

phonemes = [element for line in wordlist for element in line]

for phoneme in Counter(phonemes).most_common():
    print(phoneme)

