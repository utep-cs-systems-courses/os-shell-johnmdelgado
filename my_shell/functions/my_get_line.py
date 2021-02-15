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
from os import read, write
import sys

        
def my_get_line(bytes_size,debug):
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
                print("New line detected")
            el.evaluate_line(whole_line,debug)
            #formatted_string = "{}\n".format(whole_line)
            #write(1, formatted_string.encode())
            whole_line =""
        # if we've reached the end of the buffer and a new line character has not been detected
        # then we need to read in another 100 bytes from the buffer
        # but we also need to add the current character to the string
        elif(index == len(read_from_buffer)-1):
            read_from_buffer = gc.my_get_char(bytes_size,debug)
            if read_from_buffer is None:
                print("nothing left in the buffer!!")
                sys.exit(0)
            index = 0
            whole_line += character
            continue
        # If those conditions have not been met, then add the current character to our string        
        else:   
            whole_line += character
        index += 1