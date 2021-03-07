#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to calculate frequency and functional load of English word-initial CV sequences.

author: Andrea Ceolin
date: February 2021
'''


from collections import Counter
import math

'''
Helper functions
'''

def merge_k(word):
    return word.replace('K Y', 'KY')

'''
This is the list of consonants in the English wordlist
'''

consonants = {'Y', 'DH', 'HHW', 'T', 'D', 'W', 'L', 'K', 'N', 'HH', 'G', 'S', 'P', 'R', 'F', 'TH', 'M', 'SH', 'JH', 'B', 'V', 'CH', 'Z', 'KY'}

'''
Extract English words and counts
'''
words = []
i=0
for line in open('american_corpus.txt', 'r'):
    #We only retrieve the first pronunciation, and exclude all secondary pronunciations
    if line.split()[0][-1] != ')':
        words.append(((tuple(line.split()[1:-1]), int(line.split()[-1]))))
        #words.append(((tuple(merge_k(line).split()[1:-1]), int(line.split()[-1]))))
        i+=1
    if i>=5000:
        break

'''
Create a dictionary with the token counts of the words
'''

words_tokens = Counter()
for word in words:
    words_tokens[word[0]] += word[1]
print(sum(words_tokens.values()))

'''
Calculate token and type counts of word-initial CV sequences
'''

words_tokens_initial = Counter()
for key, count in words_tokens.items():
    #ignore words which have one phoneme only
    if len(key) > 1:
        #extract a CV word-initial sequence
        if key[0] in consonants and key[1] not in consonants:
            words_tokens_initial[(key[0], key[1])] += count

words_types_initial = Counter()
for key, count in words_tokens.items():
    #ignore words which have one phoneme only
    if len(key) > 1:
        #extract a CV word-initial sequence
        if key[0] in consonants and key[1] not in consonants:
            words_types_initial[(key[0], key[1])] += 1


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
    return str(round(sum(fl_tokens) / len(fl_tokens),4)) + '\t' +  str(round(sum(fl_type)/len(fl_type), 4))


print('%s\t%s\t%s' % (round(freq_tokens_init['K'],4), round(freq_types_init['K'],4), fl('K', ['T', 'S', 'CH', 'G', 'TH', 'D', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['T'],4), round(freq_types_init['T'],4), fl('T', ['K', 'S', 'CH', 'G', 'TH', 'D', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['S'],4), round(freq_types_init['S'],4), fl('S', ['T', 'K', 'CH', 'G', 'TH', 'D', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['CH'],4), round(freq_types_init['CH'],4), fl('CH', ['T', 'S', 'K', 'G', 'TH', 'D', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['G'],4), round(freq_types_init['G'],4), fl('G', ['T', 'S', 'CH', 'K', 'TH', 'D', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['TH'],4), round(freq_types_init['TH'],4), fl('TH', ['T', 'S', 'CH', 'G', 'K', 'D', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['D'],4), round(freq_types_init['D'],4), fl('D', ['T', 'S', 'CH', 'G', 'TH', 'K', 'SH'])))
print('%s\t%s\t%s' % (round(freq_tokens_init['SH'],4), round(freq_types_init['SH'],4), fl('SH', ['T', 'S', 'CH', 'G', 'TH', 'D', 'K'])))


'''
print(fl('P', 'B'))
print(fl('T', 'D'))
print(fl('K', 'G'))


print(freq_tokens_init['T']), print(freq_types_init['T'])
print(freq_tokens_init['K']), print(freq_types_init['K'])
fl('T', 'K')
#print(freq_tokens_init['SH']), print(freq_types_init['SH'])


#print(freq_tokens_init['K']), print(freq_types_init['K'])



print(freq_tokens_init['TH'])
print(freq_tokens_init['F'])
print(freq_types_init['TH'])
print(freq_types_init['F'])
fl('F', ['TH'])



print(freq_tokens_init['S'])
print(freq_types_init['S'])
fl('S', 'T')



print(freq_tokens_init['SH'])
print(freq_types_init['SH'])
fl('T', ['SH'])
fl('S', ['SH'])


print(freq_tokens_init['KY'])
print(freq_types_init['KY'])
print(freq_tokens_init['CH'])
print(freq_types_init['CH'])

fl('CH', ['KY'])

fl('T', ['CH'])



for word, count in words_tokens.items():
    if word[0] == 'F' or word[0] == 'TH':
        print(' '.join(word) , '\t', count)


print(freq_tokens_init['D'])
print(freq_tokens_init['G'])
print(freq_types_init['D'])
print(freq_types_init['G'])
'''

