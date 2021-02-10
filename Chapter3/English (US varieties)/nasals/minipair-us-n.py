#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script is used to retrieve the number of minimal pairs associated to each phoneme for the English (US) CHILDES data.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter, defaultdict

def minimal_pairs(wordlist, phoneme):
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
    #print number and words associated to the minimal pairs of the phoneme you are interested in
    for pair in dict:
        if phoneme in pair:
            print(pair, len(dict[pair]), dict[pair])

'''
In this case, we are interested in minimal pairs that involve vowels before nasals. We will single out these cases 
by means of a special function.
'''

def merge_n(word):
    word = word.replace('AA N', 'AAN')
    word = word.replace('AO N', 'AON')
    word = word.replace('AE N', 'AEN')
    word = word.replace('AH N', 'AHN')
    word = word.replace('AW N', 'AWN')
    word = word.replace('AY N', 'AYN')
    word = word.replace('EH N', 'EHN')
    word = word.replace('EY N', 'EYN')
    word = word.replace('IH N', 'IHN')
    word = word.replace('IY N', 'IYN')
    word = word.replace('OW N', 'OWN')
    word = word.replace('OY N', 'OYN')
    word = word.replace('UH N', 'UHN')
    word = word.replace('UW N', 'UYN')
    word = word.replace('AA M', 'AAM')
    word = word.replace('AO M', 'AOM')
    word = word.replace('AE M', 'AEM')
    word = word.replace('AH M', 'AHM')
    word = word.replace('AW M', 'AWM')
    word = word.replace('AY M', 'AYM')
    word = word.replace('EH M', 'EHM')
    word = word.replace('EY M', 'EYM')
    word = word.replace('IH M', 'IHM')
    word = word.replace('IY M', 'IYM')
    word = word.replace('OW M', 'OWM')
    word = word.replace('OY M', 'OYM')
    word = word.replace('UH M', 'UHM')
    word = word.replace('UW M', 'UYM')
    return word


wordlist =[]

for line in open('american_corpus.txt'):
    #We only retrieve the first pronunciation, and exclude all secondary pronunciations. Vowels before nasals are coded
    #as independent symbols
    if line.split()[0][-1] != ')':
        wordlist.append(merge_n(line).split()[1:-1])

'''
Double check that the size of the list is the expected one
'''

print(len(wordlist))

'''
Print the minimal pairs along with their count
'''

minimal_pairs(wordlist, 'EHN')
#minimal_pairs(wordlist, 'EHM')
#minimal_pairs(wordlist, 'EHNG')

'''
Print phoneme frequencies
'''

phonemes = [element for line in wordlist for element in line]

for phoneme in Counter(phonemes).most_common():
    print(phoneme)

