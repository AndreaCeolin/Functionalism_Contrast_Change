import random
from collections import Counter, defaultdict

grk = [line for line in open('grk_merged_corpus.txt')]
#print(grk)
eng = [line for line in open('americanEng_childes_FL.txt')]
#print(eng)

grk_vocabulary = []
for line in grk:
    for num in range(int(int(line.split()[1].rstrip())/100)):
        grk_vocabulary.append(line.split()[0])

eng_vocabulary = []
for line in eng:
    for num in range(int(line.split()[-1].rstrip())):
        if line.split()[0][-1] != ')':
            eng_vocabulary.append(tuple(line.split()[1:-1]))

print(len(grk_vocabulary))
print(len(eng_vocabulary))

vowels = {'ά', 'ό', 'ί', 'έ', 'IH', 'IY', 'AH', 'AO', 'AA', 'AW', 'EH', 'EY', 'OW', 'UH', 'UW'}

def mini_count(lexicon):
    min_pairs = set()
    for index, word1 in enumerate(lexicon):
        for index2, word2 in enumerate(lexicon[index+1:]):
            if len(word1) > 1 and len(word2) > 1:
                if (word1[0], word2[0]) in {('T', 'f'), ('f', 'T'), ('TH', 'F'), ('F', 'TH'), ('D', 'v'), ('v', 'D'), ('DH', 'V'), ('V', 'DH')}:
                    if word1[1] == word2[1] and word1[1] in vowels:
                        min_pairs.add((word1, word2))
    return len(set(min_pairs)), min_pairs

def mini_super(wordlist):
    #this splits words by length classes (length:list of words) and facilitate the search process
    word_dic = defaultdict(list)
    for word in wordlist:
        word_dic[len(word)].append(word)
    #this keeps tracks of the minimal pairs
    words = defaultdict(list)
    for word_class in word_dic:
        for index, word in enumerate(word_dic[word_class]):
            for word2 in word_dic[word_class][index+1:]:
                pairs = set([(letter1, letter2) for letter1, letter2 in zip(word,word2) if letter1 != letter2])
                if len(pairs) == 1:
                    pair = pairs.pop()
                    words[pair].append((word, word2))
    #get x-y and y-x minimal pairs line up
    dict = defaultdict(list)
    for pair in words:
        if (pair[1], pair[0]) in dict:
            dict[(pair[1], pair[0])].extend(words[pair])
        else:
            dict[pair] = words[pair]
    for pair in dict:
        if pair in {('T', 'f'), ('f', 'T'), ('TH', 'F'), ('F', 'TH'), ('D', 'v'), ('v', 'D'), ('DH', 'V'), ('V', 'DH')}:
            print(pair, len(dict[pair]), dict[pair])
    return

n_words = 50000

grk_heard = Counter([random.choice(grk_vocabulary) for num in range(n_words)])
grk_acquired = [word for word in grk_heard if grk_heard[word] > 4]
print(len(grk_acquired))
grk_th = [word for word in grk_acquired if word[0] in {'T', 'f', 'D', 'v'}]

print('Grk: ')
output = mini_count(grk_th)
#print(mini_super(grk_acquired))
#print(output[0])
for item in sorted(output[1]):
    print(item)

eng_heard = Counter([random.choice(eng_vocabulary) for num in range(n_words)])
eng_acquired = [word for word in eng_heard if eng_heard[word] > 4]
print(len(eng_acquired))
eng_th = [word for word in eng_acquired if word[0] in {'TH', 'F', 'DH', 'V'}]

print('Eng: ')
#print(mini_super(eng_acquired))
output = mini_count(eng_th)
#print(output[0])
for item in sorted(output[1]):
    print(item)





