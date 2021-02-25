#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from CHILDES.
The script requires that the Cantonese CANCORP corpus is placed in the same folder of the script.

author: Andrea Ceolin
date: February 2021
'''


from collections import Counter,defaultdict
import os
import codecs


'''
This function is needed to create a unique symbol for velar /ŋ/, represented by "ng" in the romanization adopted by CANCORP
'''

def phonemicize(word):
    word = word.replace('ng', 'N')
    return word


'''
Get all the tokens you find in child-directed speech and their frequency
'''

counter = Counter()

for name in ['ccc', 'cgk', 'ckt', 'hhc', 'lly', 'ltf', 'mhz', 'wbh']: #these are the CANCORP folders
    for file in os.listdir(name):
        '''
        A problem with Cantonese is that there are many homophones. By using the English translation, we can separate them,
        something that will be needed to perform minimal pair calculations. We do so by using a variable, "tracker", which
        will tell us whether we are in the presence of words that are associated to adult speech or not.
        When we are, tracker becomes "True", and therefore both the words and their translations are stored. 
        When we encounter child speech, tracker becomes "False", so the translation and the words are not saved.
        '''
        tracker = False
        for line in codecs.open(name + '/' + file, 'r', encoding="utf8"):
            if line[1:4] in {'MOT', 'INV', 'SIS', 'SER', 'GDM', 'UNC', 'FAT', 'SIV', 'GRM'}: #this filters out the speech of adults
                tracker = True
            elif line[1:4] == 'CHI':
                tracker = False
            elif line[1:4] == 'mor' and tracker == True:
                for token in line.split():
                    #this complex pattern is needed to retrieve the translation of the word
                    if '|' in token and '=' not in token:
                        word = phonemicize(token.split('|')[1])
                        if '-' in word:
                            word = word.split('-')[0]
                        if '&' in word:
                            word = word.split('&')[0]
                        if not word.isalpha():
                            counter['None' + ' ' + word] += 1
                    elif '|' in token and '=' in token:
                        word = phonemicize(token.split('|')[-1].split('=')[0])
                        eng = token.split('|')[-1].split('=')[1]
                        if '-' in word:
                            word = word.split('-')[0]
                        if '&' in word:
                            word = word.split('&')[0]
                        if not word.isalpha():
                            counter[eng+' '+word] += 1


'''
Every key of our dictionary currently contains each word and its translation separated by a space.
In the process of saving the words and their frequency, we can remove the English translation, which served its purpose
of keeping homophones separated.
'''

f = open('cantonese_corpus.txt', 'w')
i=0
for word, counts in counter.most_common():
    i+=1
    #here we keep the Cantonese word and we remove its translation
    f.write(word.split()[1] + ' ' + str(counts) + '\n')
    #break when you get the first 5000 words
    if i == 5000:
        break
f.close()
