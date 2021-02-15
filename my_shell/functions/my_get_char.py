""" 
FileName: my_get_char.py
Author: John Delgado
Created Date: 2/7/2021
Version: 1.0 Initial Development

This file will serve as a buffer and read in the desired number of bytes from the stdin 
file descriptor(FD=0), it will then decode the buffer and return the decoded buffer.
"""
from os import read, write
import sys

def my_get_char(bytes_size,debug):
    #initialize counter
    numReads = 1
    #initalize buffer to FD 0 with length of 100 bytes
    ibuffer = read(0, bytes_size)
    # need to decode because of ascii values
    sbuf = ibuffer.decode()
    return sbuf
    