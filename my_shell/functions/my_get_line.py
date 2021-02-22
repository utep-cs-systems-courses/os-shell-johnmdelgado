#! /usr/bin/env python3
"""  
FileName: my_get_line.py
Author: John Delgado
Created Date: 2/7/2021
Version: 1.0 Initial Development

This will utilize the my_get_char buffer and interprete the buffer and print out each line from the buffer.
If the string is too long for the buffer, then it will refresh the buffer, until a new line character is detected.
"""
from sys import stdin, stdout
from functions import my_get_char as gc
from functions import evaluate_line as el
from os import read, write,getenv
import sys

def get_prompt():
    prompt = getenv('PS1')
    if prompt is None:
        prompt = "$"
    prompt_format = "{} ".format(prompt)
    return prompt_format

        
def my_get_line(bytes_size,debug):
    prompt = get_prompt()
    read_from_buffer = gc.my_get_char(bytes_size,debug)
    if debug:
        formatted_string = "This is the current buffer:\n {}".format(read_from_buffer)
        write(2,formatted_string.encode())
    index = 0
    whole_line = ""
    while index < len(read_from_buffer):
        character = read_from_buffer[index]
        if debug:
            write(2,("Current Character: [{}]".format(character)).encode())     

        # if a new line character is dectected Evaluate the line and see if it is a command    
        if (character == "\n"):
            if debug:
                write(2,"New line detected".encode())
            write(1, prompt.encode())
            write(2, ("{}\n".format(whole_line)).encode())
            el.evaluate_line(whole_line,debug)
            #formatted_string = "{}\n".format(whole_line)
            #write(1, formatted_string.encode())
            whole_line =""   

        # If those conditions have not been met, then add the current character to our string        
        else: 
            whole_line += character
        print("here is the index: {} and here is the length of buffer: {}".format(index,len(read_from_buffer)))
        index += 1

        # if we've reached the end of the buffer and a new line character has not been detected
        # then we need to read in another 100 bytes from the buffer
        # but we also need to add the current character to the string
        if index == (len(read_from_buffer)-1):
            test_buffer = gc.my_get_char(bytes_size,debug)
            print("here is the index: {} and here is the length of test buffer: {}".format(index,len(test_buffer)))
            if len(test_buffer) == 0 :
                write(2,"nothing left in the buffer!!\n".encode())
            else:
                read_from_buffer = test_buffer
                index = 0