'''
@author: Virupaksha Swamy
@email: vswamy@usc.edu
@description: Find all anagrams of a given string
'''

import sys

def find_anagrams(str):
    if(not str):
        return []
    if(len(str) == 1):
        return [str]
    output = []    
    for i in range(0, len(str)):
        c = str[i]
        temp_str = str.replace(c, "")
        temp_output = find_anagrams(temp_str)
        for item in temp_output:
            output.append(c + item)
    return output

def find_sorted_anagrams(str):
    output = find_anagrams(str)
    return sorted(output)

def write_to_file(output, filename):
    output_file = open(filename, 'w')
    for item in output:
        output_file.write(item + "\n")
        
input = sys.argv[1]
write_to_file(find_sorted_anagrams(input), "anagram_out.txt")