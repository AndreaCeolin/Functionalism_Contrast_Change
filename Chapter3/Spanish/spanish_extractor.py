#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words from CHILDES.
The script requires that the entire CHILDES Spanish corpus is placed in the same folder of the script.
It also requires having the pronunciation dictionary "es.csv" in the same folder.
At the present day, it can be downloaded from here: https://github.com/Kyubyong/pron_dictionaries.

author: Andrea Ceolin
date: February 2021
'''

'''
CHILDES Spanish corpus
'''


from collections import Counter
import os

folders = ['Aguirre', 'BecaCESNo', 'ColMex', 'DiezItza', 'FernAguado/Ainhoa', 'FernAguado/Alejando',
            'FernAguado/Alex', 'FernAguado/Ana', 'FernAguado/Andrea', 'FernAguado/Asier',
            'FernAguado/Audrey', 'FernAguado/Benat', 'FernAguado/Cara', 'FernAguado/Cristina',
            'FernAguado/Daniel', 'FernAguado/DiegoH', 'FernAguado/DiegoU', 'FernAguado/Eider',
         'FernAguado/Eneko', 'FernAguado/Erik', 'FernAguado/Fermin', 'FernAguado/Ignacio',
        'FernAguado/Inaki', 'FernAguado/InigoG', 'FernAguado/InigoZ', 'FernAguado/Ioseba',
      'FernAguado/Itzasne', 'FernAguado/Izaa', 'FernAguado/Izascun', 'FernAguado/Jaime',
        'FernAguado/JavierA', 'FernAguado/JavierG', 'FernAguado/JavierJ', 'FernAguado/Julen',
'FernAguado/Julia', 'FernAguado/Maialen', 'FernAguado/Maite', 'FernAguado/Manel',
'FernAguado/Manuel', 'FernAguado/Maria', 'FernAguado/Marta', 'FernAguado/Noelia',
        'FernAguado/Oihane', 'FernAguado/Pello', 'FernAguado/Ruben', 'FernAguado/Sergio',
'FernAguado/SilviaG', 'FernAguado/SilviaO', 'FernAguado/Virginia', 'FernAguado/Xabier',
'FernAguado/Yago', 'Hess', 'JacksonThal', 'Koine/bre', 'Koine/elf', 'Koine/mil', 'Koine/sus',
           'Koine/vit', 'Linaza', 'LlinasOjea/Irene',  'LlinasOjea/Yasmin', 'Marrero/Alfonso',
'Marrero/Idaira', 'Marrero/Rafael', 'Montes', 'Nieva', 'OreaPine/Juan', 'OreaPine/Lucia',
           'Ornat', 'Remedi', 'Romero', 'SerraSole', 'Shiro', 'Vila']



'''
Get all the tokens you find in child-directed speech
'''



#Get all the tokens you find in the child-directed speech
def get_list():
    sentences = []
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.cha'):
                for line in open(folder+'/'+file, 'r'):
                    if line[1:4] in {'MOT', 'MAD', 'FAT', 'PAD', 'SIS', 'BRO', 'INV',
                                     'KAR', 'PAR', 'EXA', 'OBS', 'ABU', 'EXP', 'MAR',
                                     'INE', 'NAC'}: #this filters out the speech of adults in the corpus
                        sentences.extend(line[5:].strip().split())
    return sentences


'''
This function is used to obtain a phonemic transcription starting from Spanish orthography.
'''


def phonemicize(word):
    word = word.replace('ce', 'ze')
    word = word.replace('ci', 'zi')
    word = word.replace('gi', 'ji')
    word = word.replace('ge', 'je')
    word = word.replace('chi', 'Ci')
    word = word.replace('che', 'Ce')
    word = word.replace('cha', 'Ca')
    word = word.replace('cho', 'Co')
    word = word.replace('chu', 'Cu')
    word = word.replace('que', 'ce')
    word = word.replace('qui', 'ci')
    word = word.replace('gue', 'ge')
    word = word.replace('gui', 'gi')
    word = word.replace('ll', 'L')
    return word


'''
Get a dictionary of lemmas that appear in Lexique.
A lemma is defined as en entry where the first column (ortho) and the third column (lemme) are the same.
The dictionary has the lemma as a key, and its phonological form (phon) as its value.
'''


dictionary = {line.split(',')[0] for line in open('es.csv', 'r')}


'''
Get frequency counts of the words that appear in the Spanish pronunciation dictionary from CHILDES.
'''

lemma_dictionary = Counter()

i=0
for word, count in Counter(get_list()).most_common():
    #in order to store the word, it must appear in the dictionary, and start with a lowercase letter (to filter names out)
    if word in dictionary and word[0].islower():
        lemma_dictionary[phonemicize(word)] += count
        i+= 1
    if i == 5000:
        break

'''
Save the words along with their CHILDES frequencies.
'''


lemma = open('spanish_corpus.txt', 'w')


for word, count in lemma_dictionary.most_common():
    lemma.write(word + ' ' + str(count) + '\n')

lemma.close()