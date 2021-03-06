#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to calculate frequency and functional load of Cantonese word-initial CV sequences.

author: Andrea Ceolin
date: February 2021
'''


from collections import Counter
import math


'''
Helper functions
'''

def vowels(word):
    word_fix = word.replace('aa', 'A').replace('oe','O').replace('eo','E').replace('yu','U').replace('kw', 'K').replace('gw','G')
    return word_fix

'''
This is the list of consonants in the Cantonese wordlist
'''

consonants = {'n', 'm', 'h', 'g', 'N', 'j', 't', 'k', 'd', 'z', 'l', 's', 'b', 'w', 'c', 'f', 'p', 'K', 'G', '_'}

'''
Extract Cantonese words and counts
'''

words = []
for line in open('cantonese_corpus.txt', 'r'):
    words.append(vowels(line).split())


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
    # extract a CV word-initial sequence, and ignore the case in which the second segment is a tone
    if key[0] in consonants and key[1] not in consonants and key[1].isdigit() is False:
        words_tokens_initial[key[:2]] += count

words_types_initial = Counter()
for key, count in words_tokens.items():
    # extract a CV word-initial sequence, and ignore the case in which the second segment is a tone
    if key[0] in consonants and key[1] not in consonants and key[1].isdigit() is False:
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



print('%s %s %s' % (round(freq_tokens_init['k'],4), round(freq_types_init['k'],4), fl('k', ['t', 'g', 'd', 's', 'c', 'z', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['g'],4), round(freq_types_init['g'],4), fl('g', ['t', 'k', 'd', 's', 'c', 'z', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['t'],4), round(freq_types_init['t'],4), fl('t', ['g', 'k', 'd', 's', 'c', 'z', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['d'],4), round(freq_types_init['d'],4), fl('d', ['t', 'k', 'g', 's', 'c', 'z', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['s'],4), round(freq_types_init['s'],4), fl('s', ['t', 'k', 'd', 'g', 'c', 'z', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['c'],4), round(freq_types_init['c'],4), fl('c', ['t', 'k', 'd', 's', 'g', 'z', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['z'],4), round(freq_types_init['z'],4), fl('z', ['t', 'k', 'd', 's', 'c', 'g', 'K', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['K'],4), round(freq_types_init['K'],4), fl('K', ['t', 'k', 'd', 's', 'c', 'g', 'z', 'G'])))
print('%s %s %s' % (round(freq_tokens_init['G'],4), round(freq_types_init['G'],4), fl('G', ['t', 'k', 'd', 's', 'c', 'g', 'z', 'K'])))

'''

print(freq_tokens_init['d'])
print(freq_tokens_init['g'])
print(freq_types_init['d'])
print(freq_types_init['g'])
fl('d', 'g')


for key,value in Counter(words_types_initial).most_common():
    if 'd' in key or 'g' in key:
        print(key,value)


for word, count in words_tokens_initial.most_common():
    print(word,count)


print(freq_tokens_init['s'])
print(freq_types_init['s'])
fl('s', 'd')


print(freq_tokens_init['z'])
print(freq_types_init['z'])

fl('d', 'z')
fl('s', 'z')
fl('g', 'z')
'''

