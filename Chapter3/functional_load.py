#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script contains the basic functions needed to perform functional load calculations.
In this case, we apply the functions to the classic Surendran and Niyogi's toy example.

author: Andrea Ceolin
date: February 2021
'''


from collections import Counter
import math


'''
This is the toy example in Surendran and Niyogi (2006)
'''
toy = 'atuattatuatatautuaattuua'


'''
This function extracts ngrams from  text
'''

def ngrams(text, k=1):
    '''
    :param text: the input text
    :param k: the order of the Markov model
    :return: ngram counts
    '''
    counts = Counter()
    if k == 0: #return unigrams if k=0
        counts = Counter(text)
    else: #return k+1grams if k>1
        for index, letter in enumerate(text[:-k]):
            counts[text[index:index+k+1]] +=1
    return counts

'''
This function calculates entropy given an ngram distribution
'''

def entropy(text, k=1):
    '''
    :param text: the input text
    :param k: the order of the Markov model
    :return: entropy
    '''
    ngrams_dic = ngrams(text, k) #retrieves ngrams
    total = sum(ngrams_dic.values()) #ngram total
    sommation = 0
    for value in ngrams_dic.values(): #sommation
        sommation += value/total * math.log(value/total, 2)
    sommation = sommation / (k+1)
    return -sommation

'''
This function combines the previous functions to calculate entropy loss given a merger
'''

def functional_load(text, phon1, phon2):
    '''
    :param text: the input text
    :param phon1: phoneme replaced
    :param phon2: phoneme used as replacement
    :return: the different in entropy between the two states
    '''
    merged_text = text.replace(phon1, phon2)
    return (entropy(text)-entropy(merged_text))/entropy(text)


'''
Print entropy of the toy example, and entropy loss after a merger between 'a' and 'u', like in Surendran and Niyogi 2006
'''
print(entropy(toy))
print(functional_load(toy, 'a', 'u'))