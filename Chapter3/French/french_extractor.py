#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from CHILDES and Lexique.
The script requires that the entire CHILDES French corpus is placed in the same folder of the script.
It also requires having the Lexique corpus in the same folder.
At the present day, it can be downloaded from here: http://www.lexique.org
The file is called "Lexique383.tsv".

author: Andrea Ceolin
date: February 2021
'''



'''
CHILDES French corpus
'''


from collections import Counter
import os
import codecs

folders = ['Champaud', 'Geneva', 'Hammelrath',
            'Leveille', 'Lyon/Anais', 'Lyon/Marie', 'Lyon/Marilyn', 'Lyon/Nathan',
            'Lyon/Theotime', 'Palasis', 'Paris/Anae', 'Paris/Antoine',
             'Paris/Julie', 'Paris/Leonard', 'Paris/Madeleine', 'Paris/Theophile',
           'Pauline', 'Yamaguchi', 'York/Anne', 'York/Lea', 'York/Max']


'''
Get all the tokens you find in child-directed speech
'''


def get_list():
    sentences = []
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.cha'):
                for line in open(folder+'/'+file, 'r'):
                    if line[1:4] in {'MOT', 'FAT', 'OBS', 'ADU', 'MAD', 'INV', 'BRO',
                                     'CAR'}: #this filters out the speech of adults in the corpus
                        sentences.extend(line[5:].strip().split())
    return sentences


'''
Get a dictionary of lemmas that appear in Lexique.
A lemma is defined as en entry where the first column (ortho) and the third column (lemme) are the same.
The dictionary has the lemma as a key, and its phonological form (phon) as its value.
'''

lexique_lemmas = {line.split('\t')[0]:line.split('\t')[1] for line in open('Lexique383.tsv') if line.split('\t')[0]==line.split('\t')[2]}


'''
Get frequency counts of the Lexique lemmas in CHILDES
'''

lemma_dictionary = Counter()


i=0
for word, count in Counter(get_list()).most_common():
    #in order to store the word, it must appear in Lexique, and start with a lowercase letter (to filter names out)
    if word in lexique_lemmas and word[0].islower():
        lemma_dictionary[word] += count
        i+= 1
    #break when you get the first 5000 words
    if i == 5000:
        break


'''
Save the words in their phonological form, along with their CHILDES frequencies.
'''

lemmas = open('french_corpus.txt', 'w')

for word, count in lemma_dictionary.most_common():
    lemmas.write(lexique_lemmas[word] + ' ' + str(count) + '\n')

lemmas.close()