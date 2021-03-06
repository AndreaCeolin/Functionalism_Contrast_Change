#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from CHILDES.
The script requires that the entire CHILDES Japanese corpus is placed in the same folder of the script.

author: Andrea Ceolin
date: February 2021
'''


from collections import Counter,defaultdict
import os
import codecs


'''
This functions is used to encode the sequences 'sh', 'ts' and 'ch' as independent phonemes
'''


def translitterate(word):
    word = word.replace('sh', 'S')
    word = word.replace('ts', 'Z')
    word = word.replace('ch', 'C')
    return word

'''
CHILDES Japanese corpus
'''

def get_list():
    dict = Counter()
    for name in ['Hamasaki', 'Ishii', 'MiiPro/ArikaF', 'MiiPro/ArikaM', 'MiiPro/Asato', 'MiiPro/Nanami',
                 'MiiPro/Tomito', 'Miyata/Aki', 'Miyata/Ryo', 'Miyata/Tai', 'NINJAL-Okubo', 'Noji',
                 'Ogawa', 'Okayama', 'Ota/Hiromi', 'Ota/Kenta', 'Ota/Takeru', 'Yokoyama']:
        for file in os.listdir(name):
            if file.endswith('.cha'):
                for line in codecs.open(name + '/' + file, 'r', encoding="utf8"):
                    if line[1:4] in {'MOT', 'FAT'}:  #this filters out the speech of mothers and fathers
                        for word in line[5:].strip().split():
                            dict[word] += 1
    filter_dic = {translitterate(key):count for key, count in dict.most_common() if key[0].islower() and key.isalpha()}
    return filter_dic


'''
Save the words in their phonological form, along with their CHILDES frequencies.
'''

f = open('japanese_corpus.txt', 'w')
i=0
for word, count in get_list().items():
    f.write(word + ' ' + str(count) + '\n')
    i+=1
    if i>=5000:
        break
f.close()
