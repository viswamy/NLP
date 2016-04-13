'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to build the model for HMM tagging!
'''

import sys
import os
import time
import json

'''
path = sys.argv[1]

input_file = open(path, 'r')
output_file = open('out.txt', 'w')

d = {}

for line in input_file:
    line = line.replace('\n', '')
    tokens = line.split(' ')
    for i in range(0, len(tokens)):
        tag = tokens[i].split('/')[-1]
        if(tag in d):
            d[tag] += 1
        else:
            d[tag] = 1
            
print(json.dumps(d) , file=output_file)

'''


x = json.loads('{"P0": 12857, "DP": 23, "PR": 12342, "PT": 364, "WW": 2933, "FF": 139077, "II": 37, "PP": 6105, "NC": 180032, "DA": 114090, "PI": 2068, "VA": 13113, "CS": 12883, "NP": 65572, "DT": 66, "SP": 131631, "DR": 210, "RG": 26780, "AQ": 57944, "AO": 2803, "CC": 30151, "PX": 5439, "ZZ": 19254, "PD": 1150, "VM": 74908, "RN": 3497, "VS": 15010, "DI": 25368, "DD": 4285}')

print(x['P0'])