#!/usr/bin/env python3

import random

vowels = {'i': 0, 'e': 1, 'a': 2, 'o': 3, 'u': 4, 'ou':5, 'ei':6, 'ea':7, 'ee':8, 'oo':9, 'ai':10, 'oa':11,
          'oi':12, 'io':13, 'ie':14}
consonants = {'m': 0, 'p':1, 'b':2, 'f': 3, 'v': 4, 'd': 5, 't': 6, 'l': 7, 'n': 8, 'r': 9, 's': 10, 'k': 11,
              'y': 12, 'g': 13, 'j':14, 'h': 15, 'c':16, ' ':17, 'th':18, 'sh':19, 'wh':20, 'ch':21, 'tw':22,
              'x':23, 'w':24, 'z':25}

f = open('uniform-500.txt', 'w')
for _ in range(500):
    f.write('%s-%s-%s\n' % (random.choice(list(consonants)), random.choice(list(vowels)), random.choice(list(consonants))))
f.close()


