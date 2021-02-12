#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words in CHILDES and CELEX.
The script requires that the entire CHILDES German corpus is placed in the same folder of the script.
It also requires having the CELEX file 'epl.cd' in the same folder.
If you don't have access to CELEX, you can use the interface at http://celex.mpi.nl to get the German lemma lexicon.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import os
import codecs


'''
CHILDES German corpus
'''

folders = ['Caroline', 'Manuela', 'Miller/Kerstin', 'Miller/Simone', 'Stuttgart/AD', 'Stuttgart/AL', 'Stuttgart/BL', 'Stuttgart/BW', 'Stuttgart/CH',
           'Stuttgart/DB', 'Stuttgart/ED', 'Stuttgart/EL', 'Stuttgart/FZ', 'Stuttgart/HH', 'Stuttgart/LD',
           'Stuttgart/LL', 'Stuttgart/MB', 'Stuttgart/NB', 'Stuttgart/NW', 'Stuttgart/PW', 'Stuttgart/RL',
           'Stuttgart/TL', 'Stuttgart/VH', 'Stuttgart/VZ', 'Szagun/CI/Adriane', 'Szagun/CI/Anne',
            'Szagun/CI/Claudia', 'Szagun/CI/Daniel', 'Szagun/CI/Eileen', 'Szagun/CI/Erik',
            'Szagun/CI/Finn', 'Szagun/CI/Finn-Hendrik', 'Szagun/CI/Lara', 'Szagun/CI/Laura',
            'Szagun/CI/Lena', 'Szagun/CI/Maik', 'Szagun/CI/Marco', 'Szagun/CI/Marius',
            'Szagun/CI/Michelle', 'Szagun/CI/Mike', 'Szagun/CI/Nancy', 'Szagun/CI/Phillip',
            'Szagun/CI/Ricardo', 'Szagun/CI/Sara', 'Szagun/CI/Sarah', 'Szagun/CI/Silja',
            'Szagun/TD/Anna', 'Szagun/TD/Celina','Szagun/TD/Emely', 'Szagun/TD/Ems',
            'Szagun/TD/Falko', 'Szagun/TD/Finn','Szagun/TD/Ina', 'Szagun/TD/Isabel',
            'Szagun/TD/Jores', 'Szagun/TD/Konstantin','Szagun/TD/Leo', 'Szagun/TD/Leon',
            'Szagun/TD/Lisa', 'Szagun/TD/Luisa','Szagun/TD/Mario', 'Szagun/TD/Marlou',
           'Szagun/TD/Martin', 'Szagun/TD/Neele', 'Szagun/TD/Rahel', 'Szagun/TD/Sina',
            'Szagun/TD/Sino', 'Szagun/TD/Soeren',
           'TAKI/AD', 'TAKI/AL', 'TAKI/BL', 'TAKI/ED', 'TAKI/EL', 'TAKI/LD', 'TAKI/LL',
           'TAKI/RL', 'TAKI/TL', 'TAKI/VD', 'TAKI/VH',
             'Wagner', 'Weissenborn']


'''
Get all the tokens you find in child-directed speech
'''


def get_list():
    sentences = []
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.cha'):
                for line in open(folder+'/'+file, 'r'):
                    # this filters out the speech of mothers and fathers, and investigators
                    if line[1:4] in {'MAX', 'MAR', 'MUT', 'MOT', 'VAT', 'FAT', 'FAH'}:
                        sentences.extend(line[5:].strip().split())
    return sentences


'''
Get a dictionary of lemmas that appear in CELEX.
The dictionary has the lemma as a key, and its phonological form as its value
'''

celex_lemmas = {line.split('\\')[1]:line.split('\\')[3].replace("'", "").replace("-", "") for line in open('gpl.cd')}


'''
Get frequency counts of the CELEX lemmas in CHILDES
'''

lemma_dictionary = Counter()

i=0
for word, count in Counter(get_list()).most_common():
    if word in celex_lemmas:
        lemma_dictionary[word] += count
        i+= 1
    # break when you get the first 5000 words
    if i == 5000:
        break

'''
Save the words in their phonological form, along with their CHILDED frequencies.
'''

lemmas = open('german_corpus.txt', 'w')

for word, count in lemma_dictionary.most_common():
    lemmas.write(celex_lemmas[word] + ' ' + str(count) + '\n')

lemmas.close()


