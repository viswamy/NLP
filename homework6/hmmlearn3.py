'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to build the model for HMM tagging!
'''

import sys
import os
import time
import json

class Model:
        
    def __init__(self, path):
        self.path = path
        self.iv = {}
        self.tp = {}
        self.ep = {}
        self.tags = set()
        
        self.process()
        self.post_process()
        return

    def clean_line(self, line):
        line = line.replace('\n','')
        out = []
        tokens = line.split(' ')
        for token in tokens:
            t = []
            word_tag = token.split('/')
            t.append(word_tag[0])
            t.append(word_tag[-1])
            out.append(t)
        return out
        
    def process_transition_probabilities(self, line):
        initial_tag = line[0][1]
        if(initial_tag in self.iv):
            self.iv[initial_tag] += 1
        else:
            self.iv[initial_tag] = 1
        for i in range(1, len(line)):
            prev_tag = line[i-1][1]
            cur_tag = line[i][1]
            if(prev_tag not in self.tp):
                self.tp[prev_tag] = {}
            t = self.tp[prev_tag]
            if(cur_tag in t):
                t[cur_tag] += 1
            else:
                t[cur_tag] = 1
        return
        
    def process_emission_probabilities(self, line):
        for i in range(0, len(line)):
            word = line[i][0]
            tag = line[i][1]
            if(word not in self.ep):
                self.ep[word] = {}            
            t = self.ep[word]
            if(tag in t):
                t[tag] += 1
            else:
                t[tag] = 1
        return
    
    def process_tags(self, line):
        for i in range(0, len(line)):
            tag = line[i][1]
            self.tags.add(tag)
        return
         
    def process(self):
        f = open(self.path, 'r')
        for line in f:
            line = self.clean_line(line)
            self.process_transition_probabilities(line)
            self.process_emission_probabilities(line)
            self.process_tags(line)    
        return              
    
    def to_JSON(self):
        out = {}
        out["iv"] = self.iv
        out["tp"] = self.tp
        out["ep"] = self.ep
        return json.dumps(out)
    
    def post_process(self):
        for t in self.tp:
            sum = 0
            t2 = self.tp[t]
            t3 = set(t2.keys())
            d = self.tags.difference(t3)
            if(len(d) != 0):
                for x in t3:
                    t2[x] += 1
                for x in d:
                    t2[x] = 1
            for x in t2:
                sum += t2[x]
            t2["__sum__"] = sum
    
#path = 'temp.txt'
path = 'catalan_corpus_dev_tagged.txt'

start = time.clock()
x = Model(path)
print(time.clock() - start)

'''
print(x.tags)
print(x.iv)
print(x.tp)
print(x.ep)
'''

output_file = open("hmmmodel.txt", "w")
output_file.write(x.to_JSON())