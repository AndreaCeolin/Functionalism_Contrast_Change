#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the script used to extract words in CHILDES and CELEX.
The script requires that the entire CHILDES English-NA corpus is placed in the same folder of the script.
It also requires having the CELEX file 'epl.cd' in the same folder.
If you don't have access to CELEX, you can use the interface at http://celex.mpi.nl to get the English lemma lexicon.

author: Andrea Ceolin
date: February 2021
'''

from collections import Counter
import os
import cmudict

'''
CHILDES English-NA corpus
'''

folders = ['Bates/Free20', 'Bates/Free28', 'Bates/Snack28', 'Bates/Story28', 'Bernstein/Children',
           'Bernstein/Interview', 'Bliss', 'Bloom70/Eric', 'Bloom70/Gia', 'Bloom70/Peter', 'Bloom73',
           'Bohannon/Bax', 'Bohannon/Nat', 'Braunwald', 'Braunwald/0diary', 'Brent/c1', 'Brent/d1',
           'Brent/f1', 'Brent/f2', 'Brent/i1', 'Brent/j1', 'Brent/m1', 'Brent/m2', 'Brent/q1',
           'Brent/s1', 'Brent/s2', 'Brent/s3', 'Brent/t1', 'Brent/v1', 'Brent/v2', 'Brent/w1',
           'Brent/w3', 'Brown/Adam', 'Brown/Eve', 'Brown/Sarah', 'Carterette', 'Clark', 'ComptonPater/Julia',
           'ComptonPater/Sean', 'ComptonPater/Trevor', 'Cornell', 'Davis/Aaron', 'Davis/Anthony', 'Davis/Ben',
           'Davis/Cameron', 'Davis/Charlotte', 'Davis/Georgia', 'Davis/Hannah', 'Davis/Jodie', 'Davis/Kaeley',
           'Davis/Kate', 'Davis/Martin', 'Davis/Micah', 'Davis/Nate', 'Davis/Nick', 'Davis/Paxton', 'Davis/Rachel',
           'Davis/Rebecca', 'Davis/Rowan', 'Davis/Sadie', 'Davis/Sam', 'Davis/Willie', 'Demetras1',
           'Demetras2/Jimmy', 'Demetras2/Michael', 'Demetras2/Tim', 'EllisWeismer/30ec', 'EllisWeismer/30pc',
           'EllisWeismer/42ec', 'EllisWeismer/42pc', 'EllisWeismer/54ec', 'EllisWeismer/54int', 'EllisWeismer/66conv',
           'Evans/CH1', 'Evans/CH2', 'Feldman', 'Garvey/CH1', 'Garvey/CH2', 'Gathercole', 'Gelman/1998-Books',
           'Gelman/2004-Gender', 'Gelman/2014-IndDiff', 'Gleason/Dinner', 'Gleason/Father', 'Gleason/Mother',
           'Goad/Julia', 'Goad/Sonya', 'Haggerty', 'Hall/BlackPro', 'Hall/BlackWork', 'Hall/WhitePro', 'Hall/WhiteWork',
           'Higginson/April', 'Higginson/June', 'Higginson/May', 'HSLLD/HV1', 'HSLLD/HV2', 'HSLLD/HV3',
           'HSLLD/HV5', 'HSLLD/HV7', 'Inkelas/E', 'Kuczaj', 'MacWhinney', 'MacWhinney/0notrans-late',
           'McCune/Alice', 'McCune/Aurie', 'McCune/Danny', 'McCune/Jase', 'McCune/Kari', 'McCune/Nenni',
            'McCune/Nenni', 'McCune/Rala', 'McCune/Rick', 'McCune/Ronny', 'McCune/Vito', 'McMillan',
           'Morisset/Seattle', 'Morisset/Topeka', 'Morisset/UCLA', 'Nelson', 'NewEngland/14', 'NewEngland/20',
            'NewEngland/32', 'NewEngland/60', 'NewmanRatner/07', 'NewmanRatner/10', 'NewmanRatner/11',
            'NewmanRatner/18', 'NewmanRatner/24', 'NewmanRatner/interviews/07', 'NewmanRatner/interviews/10',
            'NewmanRatner/interviews/11', 'NewmanRatner/interviews/18', 'NewmanRatner/interviews/24', 'NH',
           'Normal-2', 'PaidoEnglish/2a', 'PaidoEnglish/2b', 'PaidoEnglish/3a', 'PaidoEnglish/3b',
            'PaidoEnglish/4a', 'PaidoEnglish/4b', 'PaidoEnglish/5a', 'PaidoEnglish/5b', 'Peters', 'POLER/Chronic',
           'POLER/Match', 'POLER/NewOnset', 'Post/Lew', 'Post/She', 'Post/Tow', 'Providence/Alex', 'Providence/Ethan',
            'Providence/Lily', 'Providence/Naima', 'Providence/Violet', 'Providence/William', 'Rollins',
           'Sachs', 'Sawyer', 'Snow', 'Soderstrom/Joe', 'Soderstrom/The', 'StanfordEnglish/deb', 'StanfordEnglish/emi',
            'StanfordEnglish/mol', 'StanfordEnglish/sea', 'StanfordEnglish/tim', 'Suppes', 'Tardif', 'Valian',
           'VanHouten/Threes', 'VanHouten/Twos', 'VanKleeck', 'Warren', 'Weist/Ben', 'Weist/Emily', 'Weist/Emma',
           'Weist/Jillian', 'Weist/Matt', 'Weist/Roman']

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
In order to obtain a North American English pronunciation, we need to use the CMU dictionary
'''
cmu_words = cmudict.dict()
varieties = ['', '(2)', '(3)', '(4)']

lemma_dictionary = Counter()

i=0
for word, count in Counter(get_list()).most_common():
    #in order to store the word, it must appear in CELEX, in CMU, and it has to start with a lowercase letter (to filter names out)
    if word in celex_lemmas and word in cmu_words and word[0].islower():
        i += 1
        #retrieve every pronunciation in the CMU dictionary
        for index, pronunciation in enumerate(cmu_words[word]):
            pron_standard = [phoneme[:2] for phoneme in pronunciation]
            lemma_dictionary[word + varieties[index] + ' ' + ' '.join(pron_standard)] += count
        if i == 5000:
            break

'''
Save the words in their phonological form, along with their CHILDED frequencies.
'''

lemmas = open('american_corpus.txt', 'w')

for word, count in lemma_dictionary.most_common():
    lemmas.write(word + '\t' + str(count) + '\n')

lemmas.close()

