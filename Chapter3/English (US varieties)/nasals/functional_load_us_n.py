#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script has been used perform functional load calculations on the English (US) CHILDES data.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import math

words_tokens = Counter()
for line in open('american_corpus.txt', 'r'):
    #We exclude the first (the word) and last (the frequency count) element of the line to retrieve the phonological representation
    word = tuple(line.split()[1:-1])
    #We retrieve the token counts
    counts = line.split()[-1]
    #In this case, we retrieve all the first pronunciations in CMU, excluding all those that have a (2) or (3) or (4) tag,
    #which is used for alternative pronunciations.
    if line.split()[0][-1] != ')':
        words_tokens[word] += int(counts)


print(sum(words_tokens.values()))

'''
Get the type frequencies of the corpus
The number of types is lower than 5000, because of homophones
'''

words_types = {key:1 for key in words_tokens}


'''
In order to deal with unigrams, we can calculate entropy directly given the unigram frequencies (that we extract
in the functional load function from vowels occurring before nasals). 
'''

def entropy(unigrams):
    '''
    :param unigrams: unigram frequency
    :return: entropy
    '''
    total = sum(unigrams.values())
    sommation = 0
    for value in unigrams.values():
        sommation += value/total * math.log(value/total, 2)
    return -sommation

def functional_load(words, phon1, phon2):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param phon1: phoneme replaced
    :param phon2: phoneme used as replacement
    :return: the different in entropy between the two states
    '''
    intervocalic = Counter()
    merged_words = Counter()
    for word, count in words.items():
        for index, letter in enumerate(word[:-1]):
            #with this line, we retrieve only vowels occurring before nasals
            if letter[0] in {'A', 'O', 'U', 'E', 'I'} and word[index+1] in {'N', 'M', 'NG'}:
                if letter == phon1:
                    intervocalic[(letter,)] += count
                    merged_words[(phon2,)] += count
                else:
                    intervocalic[(letter,)] += count
                    merged_words[(letter,)] += count
    print(round((entropy(intervocalic) - entropy(merged_words)) / entropy(intervocalic), 4))


'''
These numbers are slightly different than those that appear in the dissertation document, because a small bug 
was found after the publication. The results and the conclusions do not change significantly, though.
'''

functional_load(words_tokens, 'IH', 'EH')
functional_load(words_tokens, 'AE', 'EH')
functional_load(words_tokens, 'AH', 'EH')
