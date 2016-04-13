'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to build the model for HMM tagging!
'''

import sys
import os
import time
import json

class Classify:
    def __init__(self, model):
        self.model = model
        self.tp = model['tp']
        self.ep = model['ep']
        self.iv = model['iv']
        self.tags = model['tags']
        return
        
    def clean(self, line):
        line = line.replace('\n','')
        line = line.split(' ')
        return line
    
    def default_ep(self):
        x = {}
        for tag in self.tags:
            x[tag] = 1
        x['__sum__'] = len(self.tags)
        return x
        
    def process_initial_word(self, word):
        d = {}
        if(word in self.ep):
            ep_t = self.ep[word]
        else:
            ep_t = self.default_ep()
        t = 0
        v = 'none'
        for tag in self.tags:
            if(tag in ep_t):
                d[tag] = (ep_t[tag] / ep_t['__sum__']) * (self.iv[tag] / self.iv['__sum__'])
                if(d[tag] >= t):
                    t = d[tag]
                    v = tag
            else:
                d[tag] = 0 
        d['__prev__'] = 'none'
        d['__curr__'] = v
        return d
    
    def process_word(self, word, prev_dict):
        d = {}
        if(word in self.ep):
            ep_t = self.ep[word]
        else:
            ep_t = self.default_ep()
        u = 'none'
        v = 'none'
        
        for tag in self.tags:
            d[tag] = 0
            for prev_tag in self.tags:
                if(tag in ep_t):
                    temp = prev_dict[prev_tag] * (ep_t[tag] / ep_t['__sum__']) * (self.tp[prev_tag][tag] / self.tp[prev_tag]['__sum__'])
                    if(d[tag] <= temp):
                        d[tag] = temp
                        u = prev_tag
                        v = tag
        d['__prev__'] = u
        d['__curr__'] = v
        return d
    
    def get_tags(self, arr):
        i = len(arr) - 1
        out = []
        out.append(arr[i]['__curr__'])
        while(i >= 1):
            out.append(arr[i]['__prev__'])
            i -= 1
        out.reverse()
        return out
        
    def tag_content(self, line):
        tokens = self.clean(line)
        out = []
        x = self.process_initial_word(tokens[0])
        out.append(x)
        for i in range(1, len(tokens)):
            x = self.process_word(tokens[i], x)
            out.append(x)
        t = self.get_tags(out)  
        
        for i in range(0, len(tokens)):
            t[i] = tokens[i] + '/' + t[i]
            
        return str.join(' ', t)
      

model_file = open('hmmmodel.txt', 'r')
input_file = open(sys.argv[1], 'r')
output_file = open('hmmoutput.txt','w')

model = json.loads(model_file.read())

classifier = Classify(model)

print('start')
for line in input_file:
    print(classifier.tag_content(line), file=output_file)
    
print('end')