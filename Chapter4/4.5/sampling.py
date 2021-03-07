#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to sample words from child-directed speech in Greek and English.

author: Andrea Ceolin
date: February 2021
'''


import random
from collections import Counter, defaultdict


'''
Retrieve the words
'''
grk = [line for line in open('grk-corpus.txt')]
eng = [line for line in open('american_corpus.txt')]

'''
Store them in proportion to their frequency
'''
grk_vocabulary = []
for line in grk:
    for num in range(int(int(line.split()[1].rstrip())/100)):
        grk_vocabulary.append(line.split()[0])

eng_vocabulary = []
for line in eng:
    for num in range(int(line.split()[-1].rstrip())):
        if line.split()[0][-1] != ')':
            eng_vocabulary.append(tuple(line.split()[1:-1]))

print(len(grk_vocabulary))
print(len(eng_vocabulary))

'''
Store the target vowels
'''
vowels = {'ά', 'ό', 'ί', 'έ', 'IH', 'IY', 'AH', 'AO', 'AA', 'AW', 'EH', 'EY', 'OW', 'UH', 'UW'}

'''
Store every contrast among two words in a language that involve /θ/ and /f/ and a match in the first vowel.
This is our operationalization of syllable contrast
'''

def mini_count(lexicon):
    syll_con = set()
    for index, word1 in enumerate(lexicon):
        for index2, word2 in enumerate(lexicon[index+1:]):
            if len(word1) > 1 and len(word2) > 1:
                if (word1[0], word2[0]) in {('T', 'f'), ('f', 'T'), ('TH', 'F'), ('F', 'TH'), ('D', 'v'), ('v', 'D'), ('DH', 'V'), ('V', 'DH')}:
                    if word1[1] == word2[1] and word1[1] in vowels:
                        syll_con.add((word1, word2))
    return len(set(syll_con)), syll_con

'''
Retrieve minimal pairs
'''

def mini_super(wordlist):
    #this classifies words by length classes (length:list of words) and speeds up the minimal pair algorithm
    word_dic = defaultdict(list)
    for word in wordlist:
        word_dic[len(word)].append(word)
    #this keeps tracks of the minimal pairs
    words = defaultdict(list)
    for word_class in word_dic:
        for index, word in enumerate(word_dic[word_class]):
            for word2 in word_dic[word_class][index+1:]:
                # retrieve all the differences between two words of the same length
                pairs = set([(letter1, letter2) for letter1, letter2 in zip(word,word2) if letter1 != letter2])
                #if the difference is exactly in one phoneme, store it as a minimal pair
                if len(pairs) == 1:
                    pair = pairs.pop()
                    words[pair].append((word, word2))
    #since so far we stored minimal pair of the form x-y and also y-x, we need to merge them under the same key
    dict = defaultdict(list)
    for pair in words:
        if (pair[1], pair[0]) in dict:
            dict[(pair[1], pair[0])].extend(words[pair])
        else:
            dict[pair] = words[pair]
    for pair in dict:
        if pair in {('T', 'f'), ('f', 'T'), ('TH', 'F'), ('F', 'TH'), ('D', 'v'), ('v', 'D'), ('DH', 'V'), ('V', 'DH')}:
            print(pair, len(dict[pair]), dict[pair])


'''
Retrieve minimal pairs
'''

'''
Set a number of words to be sampled from the vocabulary
'''
n_words = 50000

'''
These are the word tokens which are sampled
'''
grk_tokens = Counter([random.choice(grk_vocabulary) for num in range(n_words)])
eng_tokens = Counter([random.choice(eng_vocabulary) for num in range(n_words)])

'''
These are the word types which are sampled (i.e. words that occur at least 5 times)
'''

grk_types = [word for word in grk_tokens if grk_tokens[word] > 4]
print(len(grk_types))
eng_types = [word for word in eng_tokens if eng_tokens[word] > 4]
print(len(eng_types))

'''
These are the words sampled which start with one of the two target phonemes
'''

grk_th = [word for word in grk_types if word[0] in {'T', 'f', 'D', 'v'}]
eng_th = [word for word in eng_types if word[0] in {'TH', 'F', 'DH', 'V'}]


'''
Print the syllable contrasts and the minimal pairs found within this group of words
'''

print('Grk: ')
length, pairs = mini_count(grk_th)
mini_super(grk_types)
print(length)
for item in sorted(pairs):
    print(item)

print('Eng: ')
length, pairs = mini_count(eng_th)
mini_super(eng_types)
print(length)
for item in sorted(pairs):
    print(item)





