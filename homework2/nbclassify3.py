import ast
import sys
import os
import json
import math

class Nb_classifier:
    def __init__(self, model):
        self.model = model
        
    def classify(self, file_path):
        contents = open(file_path, "r").read()
        delimiters = ['.', ',', '$', '(', ')', '!', '\n', '"', ':', ';', '!', '?', "'", '&', '%', '=', '/', '@']
        delimiters = delimiters + ['[', ']', '~']
        delimiters = delimiters + ['+', '/', '*', '-']
        delimiters = delimiters + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for delimiter in delimiters:
            contents = contents.replace(delimiter, ' ')
        tokens = contents.split(' ')
        
        negative_truthful = self.model['negative_truthful']
        negative_truthful_probability = math.log(negative_truthful['reviews_count'] / negative_truthful['total_reviews_count'])
        for item in tokens:
            if(item in negative_truthful['dictionary']):
                #print(negative_truthful['dictionary'][item] / negative_truthful['total_tokens_count'])
                negative_truthful_probability = negative_truthful_probability + math.log(negative_truthful['dictionary'][item] / negative_truthful['total_tokens_count'])
                
        positive_truthful = self.model['positive_truthful']
        positive_truthful_probability = math.log(positive_truthful['reviews_count'] / positive_truthful['total_reviews_count'])
        for item in tokens:
            if(item in positive_truthful['dictionary']):
                positive_truthful_probability = positive_truthful_probability + math.log(positive_truthful['dictionary'][item] / positive_truthful['total_tokens_count'])
                
        negative_deceptive = self.model['negative_deceptive']
        negative_deceptive_probability = math.log(negative_deceptive['reviews_count'] / negative_deceptive['total_reviews_count'])
        for item in tokens:
            if(item in negative_deceptive['dictionary']):
                #print(math.log(negative_deceptive['dictionary'][item] / negative_deceptive['total_tokens_count']))
                negative_deceptive_probability = negative_deceptive_probability + math.log(negative_deceptive['dictionary'][item] / negative_deceptive['total_tokens_count'])
                
        positive_deceptive = self.model['positive_deceptive']
        positive_deceptive_probability = math.log(positive_deceptive['reviews_count'] / positive_deceptive['total_reviews_count'])
        for item in tokens:
            if(item in positive_deceptive['dictionary']):
                positive_deceptive_probability = positive_deceptive_probability + math.log(positive_deceptive['dictionary'][item] / positive_deceptive['total_tokens_count'])
        
        #print(negative_truthful_probability)
        #print(positive_truthful_probability)
        #print(negative_deceptive_probability)
        #print(positive_deceptive_probability)
        
        if(negative_truthful_probability >= negative_deceptive_probability and negative_truthful_probability >=  positive_truthful_probability and negative_truthful_probability >= positive_deceptive_probability):
            return 'truthful negative ' + file_path
        elif(positive_truthful_probability >= positive_deceptive_probability and positive_truthful_probability >= negative_truthful_probability and positive_truthful_probability >= negative_deceptive_probability):    
            return 'truthful positive ' + file_path
        elif(negative_deceptive_probability >= negative_truthful_probability and negative_deceptive_probability >= positive_truthful_probability and negative_deceptive_probability >= positive_deceptive_probability):
            return 'deceptive negative ' + file_path
        return 'deceptive positive ' + file_path
        
def run_classifier(nb_classifier, input_path, out):
    if(os.path.isfile(input_path)):
        out.append(nb_classifier.classify(input_path))
        return
    for item in os.listdir(input_path):
        sub_path = input_path + "/" + item
        if(os.path.isfile(sub_path)):
            out.append(nb_classifier.classify(sub_path))
        else:
            run_classifier(nb_classifier, sub_path, out)

def write_to_file(output_file, out):
    for item in out:
        output_file.write(item + "\n")
        
model_file = open("nbmodel.txt","r")
input_path = sys.argv[1]
output_file = open("nboutput.txt", "w")

model = ast.literal_eval(model_file.read())
nb_classifier = Nb_classifier(model)
out = []
run_classifier(nb_classifier, input_path, out)
write_to_file(output_file, out)
