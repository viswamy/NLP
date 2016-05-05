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



max_n = 4

candidate_path = sys.argv[1]
reference_path = sys.argv[2]

#This will be file 
candidate_file = open(candidate_path, 'r')

#This can be either a file or a directory
if(os.path.isdir(reference_path)):
    reference_file = []
    for file in os.listdir(reference_path):
        if(os.path.isfile(reference_path + '/' + file)):
            reference_file.append(open(reference_path + '/' + file))
else:
    reference_file = [open(reference_path, 'r')]

ans = 0
bleu = []
for cline in candidate_file:
    r_lines = []
    for i in range(0, len(reference_file)):
        r_lines.append(reference_file[i].readline())
        
    cur_ngrams_len = 1
    while(cur_ngrams_len <= max_n):
        c_ngrams  = get_n_grams(cline, cur_ngrams_len)
        r_ngrams_res = {}
        for i in range(0, len(r_lines)):
            r_ngrams = get_n_grams(r_lines[i] , cur_ngrams_len)
            for r_ngram in r_ngrams:
                if(not r_ngram in r_ngrams_res):
                    r_ngrams_res[r_ngram] = 0
                r_ngrams_res[r_ngram] = max(r_ngrams_res[r_ngram], r_ngrams[r_ngram])
        count = 0
        for c_ngram in c_ngrams:
            if(c_ngram in r_ngrams_res):
                count += min(c_ngrams[c_ngram], r_ngrams_res[c_ngram])
        count_all = 0
        print(c_ngrams)
        for c_ngram in c_ngrams:
            count_all += c_ngrams[c_ngram]
        if(count_all != 0):
            pn = count / count_all
            if(pn > 0):
                ans += math.log(pn) / max_n
        cur_ngrams_len += 1
    bp = 1    
    bleu.append(bp * math.exp(ans))
    print(r_ngrams_res)
    
avg = float(sum(bleu)) / len(bleu)
print(bleu)
print(avg)


        
 