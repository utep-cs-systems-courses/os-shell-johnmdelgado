"""  
FileName: evaluate_line.py
Author: John Delgado
Created Date: 2/13/2021
Version: 1.0 Initial Development

Once a new line character is recoginzed, then we need to determine if the line that was read
is a command or something that needs to be done with line if there is an error this needs to be handled

GOTCHA: on line 41we have to loop through all the path variables, because
the os.execve is expecting the absoulte path of the command
so this loop goes through our path variables and appends the first word
to each of the paths to determine if any of the paths has that command
if the command is found, then it executes with the other arguements 
if not an error is output saying it could not find the executeable anywhere.
"""
import os
import sys
import re
import fileinput

def convert_line_to_array(line_to_convert):
    return line_to_convert.split()

def convert_line_to_array_of_commands(line_to_convert):
    command_array = line_to_convert.split('|')
    return command_array


def check_if_exit(line_to_evaluate):
    # this regex will check that the word exit is by itself on the line. If nothing precedes or
    # postcedes then the shell will exit
    exit_regex = "(?:^|\W)exit(?:$|\W)$"
    test_exit = re.match(exit_regex,line_to_evaluate)
    if test_exit:
        sys.exit(0)

def check_if_change_directory_command(line_to_evaluate):
    # checks if string starts with cd if it does we need to use 
    # the chdir function from pyton
    cd_regex = "^cd"
    test_cd = re.match(cd_regex, line_to_evaluate)
    if test_cd:
        #split the string to only get the path we want to change to
        path = (line_to_evaluate.split())[1]
        os.chdir(path)


def check_if_redirecting(line_to_evaluate):
    # search for the redirection character, if it exists, split on that character
    # to get the file path for the redirection
    redirect_character = ">"
    test_redirect = re.search(redirect_character,line_to_evaluate)
    if test_redirect:
        path_to_redirect = re.split(redirect_character,line_to_evaluate)[1]
        
        # stdout redirection
        os.close(1) # redirect child's stdout
        os.open(path_to_redirect, os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)

        return re.split(redirect_character,line_to_evaluate)[0]



def check_if_pipes(line_to_evaluate):
    # search the string for the pipe | character, if there is pipe character,
    # we need to call the os.pipe method and then interate through the commands
    pipe_character = "\\|"
    test_pipe = re.search(pipe_character,line_to_evaluate)
    if test_pipe is not None:
        return True
    else:
        return False

def start_pipe():
    #initialize Variables
    file_discriptor_read,file_discriptor_write = os.pipe()
    for file_descriptor in (file_discriptor_read, file_discriptor_write):
        os.set_inheritable(file_descriptor, True)
        #formatted_string = "piping file descriptors for\n read: {} \n write: {} \n".format(file_discriptor_read, file_discriptor_write)
        #os.write(2, formatted_string.encode())

    return file_discriptor_read, file_discriptor_write


def evaluate_line(line_to_evaluate,debug):
    # evaluate the line for special exit condition
    check_if_exit(line_to_evaluate)

    # check if the string is changing directories
    check_if_change_directory_command(line_to_evaluate)

    # initalize variable for piping
    shell_piping= check_if_pipes(line_to_evaluate)
    commands = []
    if shell_piping:
        commands = convert_line_to_array_of_commands(line_to_evaluate)
    else: 
        commands.append(line_to_evaluate)

    if debug:
        formatted_string = "here is the list of commands: {}".format(commands)
        os.write(2,formatted_string.encode())

    # for pipes we need to go through each command
    for command in commands: 
        if debug:
            os.write(2,("Here is the current command: {}".format(command)).encode())
        pid = os.getpid()
        if shell_piping:
            file_discriptor_read, file_discriptor_write = start_pipe()

        if debug:
            os.write(2, ("About to fork (pid: {})\n".format(pid)).encode())

        run_commands = os.fork()

        if run_commands < 0:
            os.write(2, ("fork failed, returning {}\n".format(run_commands)).encode())
            sys.exit(1)

        elif run_commands == 0:                   # child
            if debug:
                formatted_string = "Child: My pid== {}.  Parent's pid= {}\n".format(os.getpid(), pid).encode()
                os.write(2, formatted_string)

            # check if there is file redirection   
            test_redirect = check_if_redirecting(command)

            # convert the line that I've read using my_get_line and then converting to an array
            # and pass these as arguments to this loop to see if that binary exists in any
            # of the below paths
            if test_redirect:
                command = test_redirect

            args = convert_line_to_array(command)


            if shell_piping:
                # check for the last command to restore stdout
                if command == commands[-1]:
                    file_discriptor_write = os.dup(1)
                os.close(file_discriptor_read) # redirect child's stdout
                os.dup(file_discriptor_write)
                # close all piped file descriptors
                #for file_descriptor in (file_discriptor_read, file_discriptor_write):
                #    os.dup(file_discriptor_write)
                #    os.close(file_descriptor)
                os.print(2,"Hello from child!!".encode())

            # Get each of the path directories to search for binaries
            directories = re.split(":", os.environ['PATH'])
            for dir in directories: # try each directory in the path
                program_path = "{}/{}".format(dir, args[0]) # append the file trying to be executed to the path
                if debug:
                    os.write(1, ("Child:  ...trying to exec {}\n".format(program_path).encode()))
                try:
                    output = os.execve(program_path, args, os.environ) # try to exec program
                    if shell_piping:
                        os.write(file_discriptor_write,output)
                    else:
                        output

                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly
            

            formatted_string = "Whoa whoa whoa! Couldn't find: [{}] as a command! Try a different command \n".format(args[0])
            os.write(2, formatted_string.encode())
            sys.exit(1)                 # terminate with error

        else: # parent (forked ok)
            childPidCode = os.wait()
            if shell_piping:
                os.close(0)
                os.dup(file_discriptor_read)
                
                for file_descriptor in (file_discriptor_write,file_discriptor_read):
                    os.close(file_descriptor)
                for line in fileinput.input():
                    print("From child: <%s>" % line)

            if debug:                          
                os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                            (pid, run_commands)).encode())

            if childPidCode[1] > 0:
                formatted_string = "Program terminated with exit code: {}\n".format(childPidCode[1])
                os.write(2, formatted_string.encode())
            