#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
import os


'''
This is the script used to extract words in CHILDES and CELEX.
The script requires that the entire CHILDES English-UK corpus is placed in the same folder of the script.
It also requires having the CELEX file 'epl.cd' in the same folder.
If you don't have access to CELEX, you can use the interface at http://celex.mpi.nl to get the English lemma lexicon.
'''

'''
CHILDES English-UK corpus
'''

folders = ['Belfast/Barbara', 'Belfast/Conor', 'Belfast/Courtney', 'Belfast/David', 'Belfast/John',
           'Belfast/Michelle', 'Belfast/Rachel', 'Belfast/Stuart', 'Conti1/0control', 'Conti1/fatsib',
           'Conti1/fatsli', 'Conti1/motsib', 'Conti1/motsli', 'Conti1/slisib', 'Conti4/SLI-narrative',
           'Conti4/SLI-spon', 'Conti4/typ-narr', 'Conti4/typ-spon', 'Cruttenden/Jane', 'Cruttenden/Lucy',
           'Fletcher/3', 'Fletcher/5', 'Fletcher/7', 'Forrester', 'Gathburn', 'Howe', 'Korman', 'Lara',
           'Manchester-2/Anne', 'Manchester-2/Aran', 'Manchester-2/Becky', 'Manchester-2/Carl',
           'Manchester-2/Dominic', 'Manchester-2/Gail', 'Manchester-2/Joel', 'Manchester-2/John', 'Manchester-2/Liz',
           'Manchester-2/Nicole', 'Manchester-2/Ruth', 'Manchester-2/Warren', 'MPI-EVA-Manchester/Eleanor',
           'MPI-EVA-Manchester/Fraser', 'Nuffield', 'Smith/Amahl', 'Thomas', 'Tommerdahl', 'Wells/Abigail',
           'Wells/Benjamin', 'Wells/Betty', 'Wells/Darren', 'Wells/Debbie', 'Wells/Ellen', 'Wells/Elspeth',
           'Wells/Frances', 'Wells/Gary', 'Wells/Gavin', 'Wells/Geoffrey', 'Wells/Gerald', 'Wells/Harriet',
           'Wells/Iris', 'Wells/Jack', 'Wells/Jason', 'Wells/Jonathan', 'Wells/Laura', 'Wells/Lee',
           'Wells/Martin', 'Wells/Nancy', 'Wells/Neil', 'Wells/Neville', 'Wells/Olivia', 'Wells/Penny',
           'Wells/Rosie', 'Wells/Samantha', 'Wells/Sean', 'Wells/Sheila', 'Wells/Simon', 'Wells/Stella',
           'Wells/Tony']

'''
Get all the tokens you find in child-directed speech
'''

def get_list():
    sentences = []
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.cha'):
                for line in open(folder+'/'+file, 'r'):
                    if line[1:4] in {'MOT', 'FAT'}: #this filters out the speech of mothers and fathers
                        sentences.extend(line[5:].strip().split())
    return sentences

'''
Get a dictionary of lemmas that appear at least twice in CELEX.
The dictionary has the lemma as a key, and its phonological form as its value
'''

celex_lemmas = {line.split('\\')[1]:line.split('\\')[5].replace("'", "").replace("-", "") for line in open('epl.cd') if int(line.split('\\')[2]) > 1}

'''
Get frequency counts of the CELEX lemmas in CHILDES
'''
lemma_dictionary = Counter()

i=0
for word, count in Counter(get_list()).most_common():
    #in order to store the word, it must appear in CELEX, and start with a lowercase letter (to filter names out)
    if word in celex_lemmas and word[0].islower():
        lemma_dictionary[word] += count
        i+= 1
    #break when you get the first 5000 words
    if i == 5000:
        break



'''
Save the words in their phonological form, along with their CHILDED frequencies.
'''

lemmas = open('english_corpus.txt', 'w')

for word, count in lemma_dictionary.most_common():
    lemmas.write(celex_lemmas[word] + ' ' + str(count) + '\n')

lemmas.close()