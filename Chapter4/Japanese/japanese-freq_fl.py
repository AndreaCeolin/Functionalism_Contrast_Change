#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to calculate frequency and functional load of Japanese word-initial CV sequences.

author: Andrea Ceolin
date: February 2021
'''


from collections import Counter
import math


'''
Helper functions
'''

def vowels(word):
    word_fix = word.replace('aa', 'A').replace('ee','E').replace('oo','O').replace('uu','U').replace('ii', 'I')
    return word_fix

def vowels_palatal(word):
    word_fix = word.replace('ky', 'K').replace('ki', 'Ki').replace('aa', 'A').replace('ee','E').replace('oo','O').replace('uu','U').replace('ii', 'I')
    return word_fix

'''
This is the list of consonants in the Japanese wordlist
'''

consonants = {'n', 'y', 'w', 'k', 'g', 'h', 'd', 's', 't', 'm', 'j', 'x', 'S', 'C', 'f', 'b', 'Z', 'z', 'p', 'r', 'v', 'K'}

'''
Extract Japanese words and counts
'''

words = []
for line in open('japanese_corpus.txt', 'r'):
    words.append(vowels(line).split())
    #This is just for the study on K
    #words.append(vowels_palatal(line).split())

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


print('%s %s %s' % (round(freq_tokens_init['z'],4), round(freq_types_init['z'],4), fl('z', ['Z', 'j', 'C', 's', 'S', 't', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['Z'],4), round(freq_types_init['Z'],4), fl('Z', ['z', 'j', 'C', 's', 'S', 't', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['j'],4), round(freq_types_init['j'],4), fl('j', ['Z', 'z', 'C', 's', 'S', 't', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['C'],4), round(freq_types_init['C'],4), fl('C', ['Z', 'j', 'z', 's', 'S', 't', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['s'],4), round(freq_types_init['s'],4), fl('s', ['Z', 'j', 'C', 'z', 'S', 't', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['S'],4), round(freq_types_init['S'],4), fl('S', ['Z', 'j', 'C', 's', 'z', 't', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['t'],4), round(freq_types_init['t'],4), fl('t', ['Z', 'j', 'C', 's', 'S', 'z', 'd', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['d'],4), round(freq_types_init['d'],4), fl('d', ['Z', 'j', 'C', 's', 'S', 't', 'z', 'k', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['k'],4), round(freq_types_init['k'],4), fl('k', ['Z', 'j', 'C', 's', 'S', 'z', 'd', 't', 'g'])))
print('%s %s %s' % (round(freq_tokens_init['g'],4), round(freq_types_init['g'],4), fl('g', ['Z', 'j', 'C', 's', 'S', 't', 'z', 'k', 'd'])))

'''

print(freq_tokens_init['t'])
print(freq_tokens_init['k'])
print(freq_types_init['t'])
print(freq_types_init['k'])


fl('t', 'k')

'''
fl('b', 'p')
fl('t', 'd')
fl('k', 'g')
'''

for item,value in words_types_initial.most_common():
    if 'k' in item or 't' in item:
        print(item,value)

print(freq_tokens_init['s'], freq_types_init['s'])
fl('s', 't')



print(freq_tokens_init['S'], freq_types_init['S'])

fl('s', 'S')
fl('t', 'S')



fl('t', 'Z')


print(freq_tokens_init['K'])
print(freq_types_init['K'])
print(freq_tokens_init['C'])
print(freq_types_init['C'])
fl('K', 'C')


fl('t', 'C')

print(freq_tokens_init['Z'])
print(freq_types_init['Z'])

fl('t', 'Z')
fl('s', 'Z')
fl('k', 'Z')


print(freq_tokens_init['d'])
print(freq_tokens_init['g'])
print(freq_types_init['d'])
print(freq_types_init['g'])

'''