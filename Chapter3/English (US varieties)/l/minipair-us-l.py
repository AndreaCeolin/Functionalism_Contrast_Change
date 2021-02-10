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
In this case, we are interested in minimal pairs that involve vowels before liquids. We will single out these cases 
by means of a special function.
'''


def merge_l(word):
    word = word.replace('AA L', 'AAL')
    word = word.replace('AO L', 'AOL')
    word = word.replace('AE L', 'AEL')
    word = word.replace('AH L', 'AHL')
    word = word.replace('AW L', 'AWL')
    word = word.replace('AY L', 'AYL')
    word = word.replace('EH L', 'EHL')
    word = word.replace('EY L', 'EYL')
    word = word.replace('IH L', 'IHL')
    word = word.replace('IY L', 'IYL')
    word = word.replace('OW L', 'OWL')
    word = word.replace('OY L', 'OYL')
    word = word.replace('UH L', 'UHL')
    word = word.replace('UW L', 'UWL')
    return word


wordlist =[]

for line in open('american_corpus.txt'):
    #We only retrieve the first pronunciation, and exclude all secondary pronunciations. Vowels before liquids are coded
    #as independent symbols
    if line.split()[0][-1] != ')':
        wordlist.append(merge_l(line).split()[1:-1])

'''
Double check that the size of the list is the expected one
'''

print(len(wordlist))

'''
Print the minimal pairs along with their count
'''

minimal_pairs(wordlist, 'IHL')

'''
Print phoneme frequencies
'''

phonemes = [element for line in wordlist for element in line]

for phoneme in Counter(phonemes).most_common():
    print(phoneme)
