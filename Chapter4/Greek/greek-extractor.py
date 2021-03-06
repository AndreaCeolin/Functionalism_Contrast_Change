#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from SUBTLEX and GreekLex.
The script requires that the the SUBTLEX corpus and the GreekLex corpus are placed in the same folder.
The SUBTLEX corpus can be found at: https://github.com/hermitdave/FrequencyWords under content/2018/el.
The file is called 'el_50k.txt'.
GreekLex can be found at https://www.psychology.nottingham.ac.uk/greeklex/.
The file is called 'GreekLex2.csv'.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter


grk_lex = {}

'''
Extract every wordform in GreekLex, along with its transcription
'''

for line in open('GreekLex2.csv'):
    row = line.split(',')
    word, transcription = row[0], row[16]
    if word not in grk_lex:
        grk_lex[word] = transcription


subtlex = Counter()


'''
Extract SUBTLEX words and their counts, up to the most 5000 frequent ones, if they are also in GreekLex
'''

i=0
for line in open('el_50k.txt'):
    word, freq = line.split()
    #this checks if the word is in GreekLex
    if word in grk_lex:
        #retrieve the phonological transcription of the word in GreekLex
        subtlex[grk_lex[word]] += int(freq.rstrip())
        i+=1
    if i==5000:
        break

'''
Save the words in their phonological form, along with their SUBTLEX frequencies.
'''

with open('grk-corpus.txt', 'w') as f:
    for word, item in subtlex.items():
        f.write(word + '\t' + str(item) + '\n')



