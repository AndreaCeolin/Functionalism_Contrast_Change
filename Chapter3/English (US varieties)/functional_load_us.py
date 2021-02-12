#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script has been used perform functional load calculations on the English (US) CHILDES data.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import math

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
This function extracts token counts for the words in the corpus.
'''

words_tokens = Counter()
for line in open('american_corpus.txt', 'r'):
    #First, we apply the function to the word. We exclude the wordform (position 0) and the frequency count (position -1),
    #and only apply it to the phonological transcription
    word = tuple(merge_rhotic(line).split()[1:-1])
    counts = line.split()[-1]
    #We only retrieve the first pronunciation, and exclude all secondary pronunciations
    if line.split()[0][-1] != ')':
        words_tokens[word] += int(counts)

print(sum(words_tokens.values()))

'''
Get the type frequencies of the corpus
The number of types is lower than 5000, because of homophones
'''

words_types = {key:1 for key in words_tokens}


'''
These are the three main functions to extract ngrams and calculate entropy loss
'''

def ngrams(words_dic, k):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param k: the order of the Markov model
    :return: ngram counts
    '''
    counts = Counter()
    if k == 0: #return unigrams if k=0
        for word in words_dic:
            for index, letter in enumerate(word):
                counts[word[index]] += words_dic[word]
    else: #return k+1grams if k>1
        for word in words_dic:
            padded_word = tuple(["|"] + list(word) + ["|"])
            for index, letter in enumerate(padded_word[:-k]):
                counts[padded_word[index:index+k+1]] += words_dic[word]
    return counts


def entropy(words_dic, k=2):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param k: the order of the Markov model
    :return: entropy
    '''
    ngrams_dic = ngrams(words_dic, k)
    total = sum(ngrams_dic.values())
    sommation = 0
    for value in ngrams_dic.values():
        sommation += value/total * math.log(value/total, 2)
    sommation = sommation / (k+1)
    return -sommation


def functional_load(words_dic, phon1, phon2):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param phon1: phoneme replaced
    :param phon2: phoneme used as replacement
    :return: the different in entropy between the two states
    '''
    merged_words = Counter()
    for word in words_dic:
        new_word = []
        for letter in word:
            if letter == phon1:
                new_word.append(phon2)
            else:
                new_word.append(letter)
        merged_words[tuple(new_word)] += words_dic[word]
    print(round((entropy(words_dic)-entropy(merged_words))/entropy(words_dic),4))

'''
This prints the functional load for the pairs mentioned in the work
'''


functional_load(words_tokens, 'AA', 'AO')
functional_load(words_tokens, 'UH', 'AO')
functional_load(words_tokens, 'AH', 'AO')


functional_load(words_tokens, 'OY', 'ER')
functional_load(words_tokens, 'AY', 'ER')
functional_load(words_tokens, 'EY', 'ER')
functional_load(words_tokens, 'AW', 'ER')
functional_load(words_tokens, 'OW', 'ER')
functional_load(words_tokens, 'IY', 'ER')
functional_load(words_tokens, 'UW', 'AO')
