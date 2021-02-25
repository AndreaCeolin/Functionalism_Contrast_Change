#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from CHILDES and CELEX.
The script requires that the entire CHILDES Dutch corpus is placed in the same folder of the script.
It also requires having the CELEX file 'epl.cd' in the same folder.
If you don't have access to CELEX, you can use the interface at http://celex.mpi.nl to get the Dutch lemma lexicon.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import os
import codecs


'''
CHILDES Dutch corpus
'''

folders = ['Asymmetries/CK-TD', 'Asymmetries/SK-ADHD','Asymmetries/SK-TD',
           'DeHouwer/Dieter', 'DeHouwer/Katrien', 'DeHouwer/Kim', 'DeHouwer/Michiel',
           'Dutch-AarssenBos/04', 'Dutch-AarssenBos/04','Dutch-AarssenBos/05', 'Dutch-AarssenBos/06',
           'Dutch-AarssenBos/07', 'Dutch-AarssenBos/08', 'Dutch-AarssenBos/09', 'Dutch-AarssenBos/10',
           'Gillis', 'Groningen/Abel', 'Groningen/Daan', 'Groningen/Iris', 'Groningen/Josse',
            'Groningen/Matthijs', 'Groningen/Peter', 'Groningen/Tomas', 'Normal', 'Utrecht/Hein', 'Utrecht/Thomas', 'VanKampen/Laura', 'VanKampen/Sarah',
           'vanOosten/dutchmono', 'Wijnen']


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
                    if line[1:4] in {'MOT', 'FAT', 'INV', 'BRO', 'JER', 'JEA',
                                     'JOS', 'FLO', 'MAT', 'ABB', 'GER', 'MAR',
                                     'BOU', 'FRE', 'HAN', 'LEI', 'FRA', 'NIE',
                                     'BEE', 'CAR', 'IN1', 'IN2', 'JOK', 'LOE',
                                     'ANT'}:
                        sentences.extend(line[5:].strip().split())
    return sentences


'''
Get a dictionary of lemmas that appear at least twice in CELEX.
The dictionary has the lemma as a key, and its phonological form as its value
'''

celex_lemmas = {line.split('\\')[1]:line.split('\\')[3].replace("'", "").replace("-", "") for line in open('dpl.cd') if int(line.split('\\')[2]) > 1}


'''
Get frequency counts of the CELEX lemmas in CHILDES
'''

lemma_dictionary = Counter()

i=0
for word, count in Counter(get_list()).most_common():
    if word in celex_lemmas and word[0].islower():
        lemma_dictionary[word] += count
        i+= 1
    # break when you get the first 5000 words
    if i == 5000:
        break

'''
Save the words in their phonological form, along with their CHILDES frequencies.
'''

lemmas = open('dutch_corpus.txt', 'w')

for word, count in lemma_dictionary.most_common():
    lemmas.write(celex_lemmas[word] + ' ' + str(count) + '\n')

lemmas.close()



