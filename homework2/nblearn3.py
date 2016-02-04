'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Program to build the model
'''

import sys
import os
import json

class Util:
    '''Util class to filter, tokenize data'''
    def __init__(self):
        pass
    
    '''
        Take the contents of a file <in the form of a stirng> and Returns
        appropriate token with their count
    '''
    @staticmethod
    def process_content(contents):
        contents = contents.lower()
        delimiters = ['.', ',', '$', '(', ')', '!', '\n', '"', ':', ';', '!', '?', "'", '&', '%', '=', '/', '@']
        delimiters = delimiters + ['[', ']', '~']
        delimiters = delimiters + ['+', '/', '*', '-']
        delimiters = delimiters + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        dictionary = {}
        for delimiter in delimiters:
            contents = contents.replace(delimiter, ' ')
        tokens = contents.split(' ')
        for token in tokens:
            if(token == ''):
                continue
            if(token in dictionary):
                dictionary[token] = dictionary[token] + 1
            else:
                dictionary[token] = 1
        return dictionary
        
    '''
        Takes absolute_path of a regular file and Returns
        the count of words in that file..
    '''
    @staticmethod
    def get_dictionary_file(absolute_path):
        #print(absolute_path)
        dictionary = {}
        if(os.path.isfile(absolute_path)):
            file_name = absolute_path
            file_object = open(file_name, "r")
            file_contents = file_object.read()
            dictionary = Util.process_content(file_contents)
        return dictionary

    '''
        Takes two dictionaries and Returns the merged dictionary
        example: 
            d1 = {'a': 1, 'b': 3}
            d2 = {'a': 2, 'z': 5}
            output = {'a':3, 'b':3, 'z':5}
    '''
    @staticmethod
    def merge_dictionaries(d1, d2):
        output = {}
        for item in d1:
            if(item in d2):
                output[item] = d1[item] + d2[item]
            else:
                output[item] = d1[item]
        for item in d2:
            if(item not in output):
                output[item] = d2[item]
        return output
        
            
    '''
        Takes the absolute path of a directory and Returns
        the count of words in that directory <Recursively>
    '''
    @staticmethod
    def get_dictionary(absolute_path):
        dictionary = {}
        if(os.path.isfile(absolute_path)):
            if(absolute_path.split('.')[-1] != 'txt'):
                return
            if(absolute_path == 'README.txt' or absolute_path == "README.md"):
                return
            temp = Util.get_dictionary_file(absolute_path)
            dictionary = Util.merge_dictionaries(dictionary, temp)
            return dictionary
        for sub_path in os.listdir(absolute_path):
            absolute_sub_path = absolute_path + "/" + sub_path
            if(os.path.isfile(absolute_sub_path)):
                if(absolute_sub_path.split('.')[-1] != 'txt'):
                    continue
                temp = Util.get_dictionary_file(absolute_sub_path)
                dictionary = Util.merge_dictionaries(dictionary, temp)
            else:
                temp = Util.get_dictionary(absolute_sub_path)
                dictionary = Util.merge_dictionaries(dictionary, temp)
        return dictionary


    '''
        Takes absolute path of the directory and Returns
        the number of reviews within that directory Recursively
    '''
    @staticmethod
    def get_reviews_count(absolute_path):
        if(os.path.isfile(absolute_path)):
            return 1
        count = 0
        for sub_path in os.listdir(absolute_path):
            absolute_sub_path = absolute_path + "/" + sub_path
            count += Util.get_reviews_count(absolute_sub_path)
        return count

class Model:
    def __init__(self, label, path):
        self.label = label
        self.path = path
        self.reviews_count = Util.get_reviews_count(self.path)
        self.dictionary = Util.get_dictionary(self.path)
        self.prior = Util.get_reviews_count(self.path)
        return
    
    def laplace_smoothing(self):
        count = 0
        for item in self.dictionary:
            self.dictionary[item] = self.dictionary[item] + 1
        self.total_tokens_count = 0
        for item in self.dictionary:
            self.total_tokens_count += self.dictionary[item]
        return
            
    def build_model(self, all_tokens, total_reviews_count):
        self.total_reviews_count = total_reviews_count
        for item in all_tokens:
            if(item not in self.dictionary):
                self.dictionary[item] = 0
        self.laplace_smoothing()
        return
    
    def __str__(self):
        out = {}
        out['label'] = self.label
        out['path'] =self.path
        out['reviews_count'] = self.reviews_count
        out['prior'] = self.prior
        out['total_reviews_count'] = self.total_reviews_count
        out['total_tokens_count'] = self.total_tokens_count
        out['dictionary'] = self.dictionary
        return out
        

development_data_path = sys.argv[1]
negative_truthful = Model('negative_truthful' , development_data_path + '/negative_polarity/truthful_from_Web') 
negative_deceptive = Model('negative_deceptive' , development_data_path + '/negative_polarity/deceptive_from_MTurk')
positive_truthful = Model('positive_truthful' , development_data_path + '/positive_polarity/truthful_from_TripAdvisor')
positive_deceptive = Model('positive_deceptive' , development_data_path + '/positive_polarity/deceptive_from_MTurk')

all_tokens = set()
for item in negative_truthful.dictionary:
    all_tokens.add(item)
for item in negative_deceptive.dictionary:
    all_tokens.add(item)
for item in positive_truthful.dictionary:
    all_tokens.add(item)
for item in positive_deceptive.dictionary:
    all_tokens.add(item)
    
total_reviews_count = negative_truthful.reviews_count + negative_deceptive.reviews_count + positive_truthful.reviews_count + positive_deceptive.reviews_count 
negative_truthful.build_model(all_tokens, total_reviews_count)
negative_deceptive.build_model(all_tokens, total_reviews_count)
positive_truthful.build_model(all_tokens, total_reviews_count)
positive_deceptive.build_model(all_tokens, total_reviews_count)

output_file = open("nbmodel.txt", "w")
output = {}
output[negative_truthful.label] = negative_truthful.__str__()
output[negative_deceptive.label] = negative_deceptive.__str__()
output[positive_truthful.label] = positive_truthful.__str__()
output[positive_deceptive.label] = positive_deceptive.__str__()


output_file.write(str(output))