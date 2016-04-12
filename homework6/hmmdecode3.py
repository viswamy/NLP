'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to build the model for HMM tagging!
'''

import sys
import os
import time
import json

model = open('hmmmodel.txt', 'r')
input_file = open(sys.argv[1], 'r')
output_file = open('hmmoutput.txt','w')


print('yo', file=output_file)     