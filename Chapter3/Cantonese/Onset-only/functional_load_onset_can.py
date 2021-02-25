#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script has been used perform functional load calculations on CANCORP.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import math

'''
Get the token frequencies of the corpus
'''
words_tokens = Counter()
for line in open('cantonese_corpus.txt', 'r'):
    word, counts = line.split()
    words_tokens[word] += int(counts)

print(sum(words_tokens.values()))

'''
Get the type frequencies of the corpus
The number of types is lower than 5000, because of homophones
'''

words_types = {key:1 for key in words_tokens}

print(sum(words_types.values()))

'''
These are the main functions to extract ngrams and calculate entropy loss
'''

def entropy(words_dic, k=0):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param k: the order of the Markov model
    :return: entropy
    '''
    total = sum(words_dic.values()) #ngram total
    sommation = 0
    for value in words_dic.values(): #sommation
        sommation += value/total * math.log(value/total, 2)
    sommation = sommation / (k+1)
    return -sommation

def functional_load_onset(words_dic, phon1, phon2):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param phon1: phoneme replaced
    :param phon2: phoneme used as replacement
    :return: the different in entropy between the two states
    '''
    merged_words = Counter()
    for word, count in words_dic.items():
        new_word = ''
        #ignore the last letter of the word, which is the tone
        for index, letter in enumerate(word[:-1]):
            #if the following letter is a tone, then the current letter must be ignored, because it is a coda
            if word[index+1].isdigit():
                new_word += letter
            elif letter in {phon1, phon2}:
                new_word += '#'
            else:
                new_word += letter
        #add the last letter
        new_word += word[-1]
        merged_words[new_word] += count
    print(round((entropy(words_dic)-entropy(merged_words))/entropy(words_dic),4))

'''
This prints the functional load for the pairs mentioned in the work
'''


functional_load_onset(words_tokens, 'n', 'l')
functional_load_onset(words_tokens, 'n', 'd')
functional_load_onset(words_tokens, 'n', 't')
functional_load_onset(words_tokens, 'n', 's')
functional_load_onset(words_tokens, 'n', 'z')
functional_load_onset(words_tokens, 'n', 'c')