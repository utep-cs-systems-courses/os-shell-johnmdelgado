# My read line 
This module is making using of os level file descriptors(0 and 1) to read from the input from FD0 and then output to FD1, by reading from a buffer of n size and then reading from that buffer until a new line character is found.

## Project 
Write a method called myreadline() that
Returns the next line obtained from fd 0 as a string
An empty string if EOF is reached 

my_getchar() should call os.read()
my_getline() can call my_getchar() (or if you're ambitious) os.read()

## Purpose 
The point of this lab is for your character & string reading code to rely ONLY on os.read() to obtain input characters.

## Getting started 
## Built with
[Python 3.7.3](https://www.python.org/downloads/release/python-373/)

## Prerequisites
### Python Version 3.7.3
    sudo apt-get update
    sudo apt-get install python3.7.3
### Python yaml package
    sudo apt-get install python-yaml
    sudo yum install python-yaml

## Configuration
Under the configs folder is the config.yaml file with configuration settings. These are the default values but can be updated as needed or as requirements change. 


## Examples of use 
**Notes**
* In the repo there is a test_file.txt under the data directory that you can use and or modify or it will prompt you for input(see below).  
* You can also use a custom txt file containing passwords that are common or want to be exempted. Included in this package under the data folder is a common_passwords.txt that will be used by default if there isn't a txt file specifed.
### Without providing a file 

```sh
python3 my_read_line.py
```

This will fun the main executable file and prompt you to enter input into the command line to interpret. Pressing enter in this prompt will tell the module that you are done entering input and to process what has been entered so far

### With providing a file
```sh
python3 my_read_line.py < ./data/test_file.txt
```

This will run the main executable file and take in a file to FD0

## References 
* [Using os.read to read n bytes](https://www.geeksforgeeks.org/python-os-read-method/#:~:text=read()%20method%20in%20Python,bytes%20left%20to%20be%20read)
* [Interview Project](https://github.com/johnmdelgado/SRE-Project)

## License  
Distributed under the MIT License. See `LICENSE` for more information.
