'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to compute BLEU score
'''

import sys
import os
import time
import json
import math



'''
    Takes a list of strings and returns total number of words in it
'''
def getlen(l):
    count = 0
    for item in l:
        count += len(item.split(' '))
    return count



'''
    takes a string and n
    returns a list of all n-grams in the given string where!
'''
def get_n_grams(s, n):
    words = s.split(' ')
    n_grams = {}
    
    i = 0
    while(i + n <= len(words)):
        t = ' '.join(words[i : i + n])
        if(not t in n_grams):
            n_grams[t] = 0
        n_grams[t] += 1
        i += 1
    return n_grams



candidate_path = sys.argv[1]
reference_path = sys.argv[2]

#This will be file 
candidate_file = open(candidate_path, 'r')

#This can be either a file or a directory
if(os.path.isdir(reference_path)):
    reference_files = []
    for file in os.listdir(reference_path):
        if(os.path.isfile(reference_path + '/' + file)):
            reference_files.append(open(reference_path + '/' + file))
else:
    reference_files = [open(reference_path, 'r')]

c_sentences = candidate_file.read().splitlines()
r_sentences = []
for i in range(0, len(reference_files)):
    r_sentences.append(reference_files[i].read().splitlines())


max_n = 4
cur_ngrams_len = 1
bleu = 0
while(cur_ngrams_len <= max_n):
    clip_count = 0
    count = 0
    for i in range(0, len(c_sentences)):
        c_ngrams = get_n_grams(c_sentences[i], cur_ngrams_len)
        
        max_r_grams = {}
        for k in range(0, len(r_sentences)):
            r_ngrams = get_n_grams(r_sentences[k][i], cur_ngrams_len)
            for ngram in r_ngrams:
                if(not ngram in max_r_grams):
                    max_r_grams[ngram] = 0
                max_r_grams[ngram] = max(max_r_grams[ngram], r_ngrams[ngram])
        
        for ngram in c_ngrams:
            count += c_ngrams[ngram]
            if(ngram in max_r_grams):
                clip_count += min(c_ngrams[ngram], max_r_grams[ngram])
                
    pn = float(clip_count) / count
    #print(str(pn) + ',' + str(clip_count) + ',' + str(count) + ',' + str(cur_ngrams_len))
    if(pn > 0):
        bleu += (1 / max_n) * math.log(pn)
    cur_ngrams_len += 1
    
bleu = math.exp(bleu)


c_sentences_len = getlen(c_sentences)
min = 9999999999999
r_sentences_len = 0

for i in range(0, len(r_sentences)):
    r_sentences_len_t = getlen(r_sentences[i])
    if(abs(c_sentences_len - r_sentences_len_t) < min):
        min = abs(c_sentences_len - r_sentences_len_t)
        r_sentences_len = r_sentences_len_t

bp = 1
if(c_sentences_len <= r_sentences_len):
    bp = math.exp(1 - float(r_sentences_len) / c_sentences_len)

bleu = bp * bleu

print(bleu)

output_file = open('bleu_out.txt', 'w')
output_file.write(str(bleu))