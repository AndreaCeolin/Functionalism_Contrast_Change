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
In order to deal with unigrams, we can calculate entropy directly given the unigram frequencies (that we extract
in the functional load function from vowels occurring before intervocalic 'R'). 
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
            #with this line, we retrieve only vowels occurring before intervocalic 'R'
            if letter[0] in {'A', 'O', 'U', 'E', 'I'} and letter[-1] == 'R' and word[index+1][0] in {'A', 'O', 'U', 'E', 'I'}:
                if letter == phon1:
                    intervocalic[(letter,)] += count
                    merged_words[(phon2,)] += count
                else:
                    intervocalic[(letter,)] += count
                    merged_words[(letter,)] += count
    print(round((entropy(intervocalic)-entropy(merged_words))/entropy(intervocalic),4))


'''
These numbers are different than those that appear in the dissertation document, because a bug was found after
the publication. The results and the conclusions do not change significantly, though.
'''


functional_load(words_tokens, 'AHR', 'ER')
functional_load(words_tokens, 'EHR', 'AER')
functional_load(words_tokens, 'EHR', 'EYR')
functional_load(words_tokens, 'EHR', 'AHR')
functional_load(words_tokens, 'IHR', 'IYR')
functional_load(words_tokens, 'EHR', 'ER')
functional_load(words_tokens, 'AER', 'ER')
functional_load(words_tokens, 'EYR', 'ER')
functional_load(words_tokens, 'IHR', 'ER')
functional_load(words_tokens, 'EHR', 'IHR')
functional_load(words_tokens, 'EYR', 'IHR')
functional_load(words_tokens, 'AER', 'AHR')


functional_load(words_tokens, 'AER', 'AAR')
functional_load(words_tokens, 'AOR', 'AAR')
functional_load(words_tokens, 'AOR', 'UHR')
functional_load(words_tokens, 'AHR', 'AAR')
functional_load(words_tokens, 'AHR', 'AOR')
functional_load(words_tokens, 'EYR', 'IHR')
functional_load(words_tokens, 'ER', 'AAR')
functional_load(words_tokens, 'ER', 'AOR')

