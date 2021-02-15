"""  
FileName: my_read_line.py
Author: John Delgado
Created Date: 2/7/2021
Version: 1.0 Initial Development

This is the main executeable file for the module
"""

from functions import my_get_line as gl
from functions import get_config as mc
from os import write
import sys
import os
if __name__ == '__main__':

    config = mc.get_config()

    #inialize variables from config file
    debug = config["debugging"]["debug"]
    bytes_to_read = config["defaults"]["bytesToRead"]
    prompt_string = config["defaults"]["promptString"] +""

    if debug:
        print(f"Stdin uses file descriptor {sys.stdin.fileno()}\n")
        print(f"Stdout uses file descriptor {sys.stdout.fileno()}\n")
    #get filedescriptors for stdin/stdout
    while 1:
        write(1, prompt_string.encode())
        gl.my_get_line(bytes_to_read,debug)


    

