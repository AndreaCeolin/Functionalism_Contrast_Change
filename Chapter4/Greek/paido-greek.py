#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract the elicitation of the children of the PAIDOLOGOS corpus.
The script requires that the entire CHILDES PaidoGreek corpus is placed in the same folder of the script.
The corpus can be downloaded from the following link: https://phonbank.talkbank.org/access/Other/Greek/PaidoGreek.html

author: Andrea Ceolin
date: February 2021
'''

import os
from collections import Counter


target = False
target_word = False
counter = Counter()

#this part iterates through the elicitation of the children in the groups 2a, 2b, 3a, and 3b, the 2;00-4;00 interval
for group in {'2a', '2b', '3a', '3b'}:
    for file in os.listdir('PaidoGreek/' + group + '/'):
        for line in open('PaidoGreek/' + group + '/' + file):
            #this line records the word being elicited
            if line[:5] == '*CHI:':
                target_word = line.split()[1]
            #this line records the first target phoneme
            elif line[:5] == '%xwbs':
                target = line.split()[1]
            #this line records the elicitation of the word by the chld
            elif line[:5] == '%xtr:':
                if target == 's':
                #if target == 't':
                #if target == 'C':
                #if target == 'k':
                #if target == 'T':
                #if target == 'ts':
                #if target == 'x':
                #if target == 'sh':

                # this line prints all the data of the elicitation, which will be used for the regression analysis
                    print('Greek', '\t', group, '\t', target, '\t', target_word, '\t', line.split()[1], '\t', file)
                    counter[line.split()[1]] += 1

'''
Print the elicitations, along with their frequency
'''

for item, num in sorted(counter.items()):
    print(' ' + item + '\t' + str(num))
print(sum(counter.values()))