#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
import math

'''
Since the CMU dictionary encodes the phoneme we are interested in as two separate symbols 'HH' and 'W', we need
a function to merge them
'''

def merge_w(word):
    return word.replace('HH W ', 'HHW ')

'''
In the CMU dictionary, pronunciations with the form 'HH W' are listed as the last entry among all possible ones.
For this reason, we need to through all the alternative pronunciations, and store only the last one
'''

words_counts = []
for line in open('american_corpus.txt', 'r'):
    #If there is an alternative pronunciation (the variety ends with the symbol ')'), the alternative pronunciaton
    #replaces the original one. This applies recursively: if there are 3 or 4 different pronunciations, only the last
    #one is retrieved, since that is the one that contains the 'HH W' symbols.
    if line.split()[0][-1] == ')':
        words_counts.pop()
        #we apply the function to retrieve the HHW symbol, and we exclude the first (the word)
        #and last (the frequency count) element of the line. This last one is stored separately
        words_counts.append(((tuple(merge_w(line).split()[1:-1]), int(line.split()[-1]))))
    else:
        words_counts.append(((tuple(merge_w(line).split()[1:-1]), int(line.split()[-1]))))

words_tokens = Counter()
for word, count in words_counts:
    words_tokens[word] = int(count)

print(sum(words_tokens.values()))

'''
Get the type frequencies of the corpus
The number of types is lower than 5000, because of homophones
'''

words_types = {key:1 for key in words_tokens}


'''
These are the two main functions to extract ngrams and calculate entropy
'''

def ngrams(words_dic, k):
    counts = Counter()
    if k == 0:
        for word in words_dic:
            for index, letter in enumerate(word):
                counts[word[index]] += words_dic[word]
    else:
        for word in words_dic:
            padded_word = tuple(["|"] + list(word) + ["|"])
            for index, letter in enumerate(padded_word[:-k]):
                counts[padded_word[index:index+k+1]] += words_dic[word]
    return counts


def entropy(words_dic, k=2):
    ngrams_dic = ngrams(words_dic, k)
    total = sum(ngrams_dic.values())
    sommation = 0
    for value in ngrams_dic.values():
        sommation += value/total * math.log(value/total, 2)
    sommation = sommation / (k+1)
    return -sommation


def functional_load(words_dic, phon1, phon2):
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
This prints the frequency of the phonemes at the type level
'''

letters = Counter()
for key in words_types:
    letters[key[0]] +=1

print(letters.items())


'''
This prints the functional load for the pairs mentioned in the work
'''


functional_load(words_tokens, 'W', 'HHW')
functional_load(words_tokens, 'V', 'HHW')
functional_load(words_tokens, 'F', 'HHW')
functional_load(words_tokens, 'HH', 'HHW')
functional_load(words_tokens, 'B', 'HHW')
functional_load(words_tokens, 'P', 'HHW')
