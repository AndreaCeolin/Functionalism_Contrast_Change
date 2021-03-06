#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to calculate frequency and functional load of Greek word-initial CV sequences.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import math


'''
This is the list of consonants in the Greek wordlist
'''

consonants = {'D', 'T', 's', 't', 'p', 'l', 'j', 'b', 'k', 'n', 'x', 'v', 'f', 'z', 'c', 'J', 'r', 'X', 'g', 'N', 'd', 'Z', 'L', 'm'}

'''
Extract Japanese words and counts
'''

words = []
for line in open('grk-corpus.txt', 'r'):
    words.append(line.replace('ts', 'Z').split())


'''
Create a dictionary with the token counts of the words
'''

words_tokens = Counter()
for word in words:
    words_tokens[word[0]] += int(float(word[1]))
print(sum(words_tokens.values()))

'''
Calculate token and type counts of word-initial CV sequences
'''

words_tokens_initial = Counter()
for key, count in words_tokens.items():
    #ignore words which have one phoneme only
    if len(key) > 1:
        # extract a CV word-initial sequence
        if key[0] in consonants and key[1] not in consonants:
            words_tokens_initial[key[:2]] += count

words_types_initial = Counter()
for key, count in words_tokens.items():
    #ignore words which have one phoneme only
    if len(key) > 1:
        # extract a CV word-initial sequence
        if key[0] in consonants and key[1] not in consonants:
            words_types_initial[key[:2]] += 1

'''
Print token and type counts of word-initial CV sequences
'''

print(sum(words_tokens_initial.values()))
print(sum(words_types_initial.values()))

'''
Print the CV sequences extracted
'''

print(words_types_initial.keys())


'''
Calculate relative frequency of word-initial consonants 
'''

freq_tokens_init = Counter()
for key, count in words_tokens_initial.items():
    freq_tokens_init[key[0]] += count
total = sum(freq_tokens_init.values())
for key in freq_tokens_init:
    freq_tokens_init[key] /= total


freq_types_init = Counter()
for key, count in words_types_initial.items():
    freq_types_init[key[0]] += count
total = sum(freq_types_init.values())
for key in freq_types_init:
    freq_types_init[key] /= total



'''
These are the main functions used to calculate functional load
'''

def entropy(words_dic, k=1):
    '''
    :param words_dic: a dictionary containing words and their corpus frequency
    :param k: the order of the Markov model
    :return: entropy
    '''
    total = sum(words_dic.values())
    sommation = 0
    for value in words_dic.values():
        sommation += value/total * math.log(value/total, 2)
    sommation = sommation / (k + 1)
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
    return round((entropy(words_dic)-entropy(merged_words))/entropy(words_dic),4)

def fl(phon1, phonlist):
    fl_tokens = []
    for phon2 in phonlist:
        fl_tokens.append(functional_load(words_tokens_initial, phon1, phon2))
    fl_type = []
    for phon2 in phonlist:
        fl_type.append(functional_load(words_types_initial, phon1, phon2))
    return str(round(sum(fl_tokens) / len(fl_tokens),4)) + ' ' +  str(round(sum(fl_type)/len(fl_type), 4))



print('%s %s %s' % (round(freq_tokens_init['s'],4), round(freq_types_init['s'],4), fl('s', ['x', 't', 'X', 'k', 'T', 'Z'])))
print('%s %s %s' % (round(freq_tokens_init['t'],4), round(freq_types_init['t'],4), fl('t', ['s', 'x', 'X', 'k', 'T', 'Z'])))
print('%s %s %s' % (round(freq_tokens_init['X'],4), round(freq_types_init['X'],4), fl('X', ['s', 't', 'x', 'k', 'T', 'Z'])))
print('%s %s %s' % (round(freq_tokens_init['k'],4), round(freq_types_init['k'],4), fl('k', ['s', 't', 'X', 'x', 'T', 'Z'])))
print('%s %s %s' % (round(freq_tokens_init['T'],4), round(freq_types_init['T'],4), fl('T', ['s', 't', 'X', 'k', 'x', 'Z'])))
print('%s %s %s' % (round(freq_tokens_init['Z'],4), round(freq_types_init['Z'],4), fl('Z', ['s', 't', 'X', 'k', 'x', 'T'])))
print('%s %s %s' % (round(freq_tokens_init['x'],4), round(freq_types_init['x'],4), fl('x', ['s', 't', 'X', 'k', 'Z', 'T'])))



'''
#fl('s', 'T')
#fl('Z', 't')


print(freq_tokens_init['t'])
print(freq_tokens_init['k'])
print(freq_types_init['t'])
print(freq_types_init['k'])

fl('t', 'k')


print(freq_tokens_init['s'])
print(freq_types_init['s'])
fl('s', 't')


print(freq_tokens_init['T'])
print(freq_tokens_init['f'])
print(freq_types_init['T'])
print(freq_types_init['f'])
fl('f', 'T')


print(freq_tokens_init['Z'])
print(freq_types_init['Z'])

fl('t', 'Z')
fl('s', 'Z')
fl('k', 'Z')


for word, count in words_tokens.items():
    if word[0] == 'f' or word[0] == 'T':
        print(word, '\t', count)
'''