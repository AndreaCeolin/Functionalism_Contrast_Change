#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script is used to retrieve the number of minimal pairs associated to each phoneme for the English (US) CHILDES data.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter, defaultdict

def minimal_pairs(wordlist, phoneme):
    '''
    :param wordlist: this is the file containing the corpus
    :param phoneme: this is the phoneme of which we want to retrieve the minimal pairs
    :return: None
    '''
    #this classifies words by length classes (length:list of words) and speeds up the minimal pair algorithm
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
Since the CMU dictionary does not take into account the allophonic variation in rhotic environments,
we need to treat vowels occurring in rhotic environments as independent symbols, in order to study mergers
like the cot/caught merger. We will do it by means of a special function.
'''

def merge_rhotic(word):
    word = word.replace('AA R', 'AAR')
    word = word.replace('AO R', 'AOR')
    word = word.replace('AE R', 'AER')
    word = word.replace('AH R', 'AHR')
    word = word.replace('AW R', 'AWR')
    word = word.replace('AY R', 'AYR')
    word = word.replace('EH R', 'EHR')
    word = word.replace('EY R', 'EYR')
    word = word.replace('IH R', 'IHR')
    word = word.replace('IY R', 'IYR')
    word = word.replace('OW R', 'OWR')
    word = word.replace('OY R', 'OYR')
    word = word.replace('UH R', 'UHR')
    word = word.replace('UW R', 'UWR')
    return word

'''
In the CMU dictionary, pronunciations with the form 'HH W' are listed as the last entry among all possible ones.
For this reason, we need to go through all the alternative pronunciations, and stores only the last one
'''

wordlist =[]

for line in open('american_corpus.txt'):
    #We only retrieve the first pronunciation, and exclude all secondary pronunciations. Rhothic environments are coded
    #as independent symbols
    if line.split()[0][-1] != ')':
        wordlist.append(merge_rhotic(line).split()[1:-1])

'''
Double check that the size of the list is the expected one
'''

print(len(wordlist))

'''
Print the minimal pairs along with their count
'''

minimal_pairs(wordlist, 'OY')

'''
Print phoneme frequencies
'''

phonemes = [element for line in wordlist for element in line]

for phoneme in Counter(phonemes).most_common():
    print(phoneme)

