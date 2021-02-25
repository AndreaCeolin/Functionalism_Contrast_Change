#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from the Slovak National Corpus.
The corpus can be accessed via free registration at the following website:

https://korpus.sk/index_en.html

This script requires that you get the lemma wordlist, with word frequency, of the corpus "prim-8.0-public-sane".

author: Andrea Ceolin
date: February 2021
'''



from collections import Counter


slovak = Counter()

i=0
for line in open('wl.tsv'): #this is the name of the tsv file that contains the corpus
    i+=1
    if i>8 and len(line.split())==2:   #this is used to filter out the first rows, which contains some extra info
        word, count = line.split()
        slovak[word] += int(count.strip('\n'))


'''
Get frequency counts in a dictionary
'''

lemma_dictionary = Counter()

i=0
for word, count in slovak.most_common():
    #the words must start with a lowercase letter (to filter names out)
    if word[0].islower():
        lemma_dictionary[word] += count
        i+= 1
    #break when you get the first 5000 words
    if i == 5000:
        break


lemmas = open('slovak_corpus.txt', 'w')

for word, count in lemma_dictionary.most_common():
    lemmas.write(word + ' ' + str(count) + '\n')

lemmas.close()

