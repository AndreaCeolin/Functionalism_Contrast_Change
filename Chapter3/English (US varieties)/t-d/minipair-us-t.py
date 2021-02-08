#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script is used to retrieve the number of minimal pairs associated to each phoneme for the English (US) CHILDES data.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter, defaultdict

'''
Since we need to isolate minimal pairs where the contrast is intervocalic, we need to keep track of vowels
'''

vowels = {'AH', 'AA', 'AO', 'AY', 'AW', 'AE', 'EH', 'EY', 'ER', 'OW', 'OH', 'OY', 'UY', 'UW', 'UH', 'IY', 'IH'}

def minimal_pairs(wordlist,phoneme):
    '''
    :param wordlist: this is the file containing the corpus
    :param phoneme: this is the phoneme of which we want to retrieve the minimal pairs
    :return: None
    '''
    #this classifies words by length classes (length:list of words) and speeds up the minimal pair algorithm
    word_dic = defaultdict(list)
    for word in wordlist:
        word_dic[len(word)].append(word)
    #this keeps tracks of the minimal pairs
    words = defaultdict(list)
    for word_class in word_dic:
        for index, word in enumerate(word_dic[word_class]):
            for word2 in word_dic[word_class][index+1:]:
                #retrieve all the differences between two words of the same length
                pairs = [(letter1, letter2) for letter1, letter2 in zip(word,word2) if letter1 != letter2]
                #if the difference is exactly in one phoneme, store it as a minimal pair
                if len(pairs) == 1:
                    #the minimal pair is stored only if the difference is intervocalic
                    for i, letter in enumerate(word[1:-1]):
                        if letter != word2[i+1]:
                            if word2[i] in vowels and word2[i+2] in vowels:
                                pair = pairs.pop()
                                words[pair].append((word, word2))
    #since so far we stored minimal pair of the form x-y and also y-x, we need to merge them under the same key
    dict = defaultdict(list)
    for pair in words:
        if (pair[1], pair[0]) in dict:
            dict[(pair[1], pair[0])].extend(words[pair])
        else:
            dict[pair] = words[pair]
    #print number and words associated to the minimal pairs
    for pair in dict:
        if phoneme in pair:
            print(pair, len(dict[pair]), dict[pair])
    return


wordlist =[]
for line in open('american_corpus.txt'):
    #In this case, we retrieve all the first pronunciations in CMU, excluding all those that have a (2) or (3) or (4) tag,
    #which is used for alternative pronunciations.
    #We exclude the first (the word) and last (the frequency count) element of the line
    if line.split()[0][-1] != ')':
        wordlist.append(line.split()[1:-1])

'''
Double check that the size of the list is the expected one
'''
print(len(wordlist))


'''
Print the minimal pairs along with their count
'''
minimal_pairs(wordlist, 'T')


'''
Print phoneme frequencies
'''

phonemes = [element for line in wordlist for element in line]

for phoneme in Counter(phonemes).most_common():
    print(phoneme)



