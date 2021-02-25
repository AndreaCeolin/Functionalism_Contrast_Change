#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script is used to retrieve the number of minimal pairs associated to each phoneme for the English (UK) CHILDES data.

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
                pairs = set()
                for pos, (letter1,letter2) in enumerate(zip(word[:-1],word2[:-1])):
                    #this retrieves a contrast which is not in coda
                    if letter1 != letter2 and not word[pos+1].isdigit() and not word2[pos+1].isdigit():
                        pairs.add((letter1, letter2))
                    #if the phonemes match, there is no need to do anything
                    elif letter1 == letter2:
                        pass
                    #if the contrast is in coda, keep track of it, but it should not add up to the minimal pair count
                    else:
                        pairs.add(('#', '#'))
                #if the final tone is different, this should also count against a minimal pair in onset position
                if word[-1] != word2[-1]:
                    pairs.add(('#', '#'))
                #if given all these conditions the difference is exactly in one phoneme, store it as a minimal pair
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


wordlist = []

for word in open('cantonese_corpus.txt'):
    wordlist.append(word.split()[0])

'''
Double check that the size of the list is the expected one
'''
print(len(wordlist))


'''
Print the minimal pairs along with their count.
Post-publication, it was noted that the contrasts between "n" and "t" are 12 instead of 13.

'''

minimal_pairs(wordlist, 'n')


'''
Print phoneme frequencies
'''

phonemes = [element for line in wordlist for element in line]

for phoneme in Counter(phonemes).most_common():
    print(phoneme)

