#! /usr/bin/env python3

import os, sys, time, re, fileinput

#Telling the user what to type to exit
print ("(Type Exit to quit.)")


while True: #keeps the program alive as long as user doesn't explicitly exit

    #Reads user inputs and commands
    os.write(1, ("PROMPT> ").encode())
    command = os.read(0, 100)

    #Checks if user typed exit
    isExit = command.decode()
    isExit = isExit[:4]
    isExit = isExit.lower()
    if isExit == "exit":
        sys.exit(1)
    
    #Sets flags to later check command contains a pipe
    sCommand = ""
    isPipe = False
    command = command.decode()
    if "|" in command:
        isPipe = True
        command, sCommand = command.split("|")
        command = command.strip()
        sCommand = sCommand.strip()

    #Create the pipe
    r, w = os.pipe()
    for f in (r, w):
        os.set_inheritable(f, True)
    rc = os.fork()

    if rc < 0:
        os.write(2, ("Failed. Now exiting.").encode())
        sys.exit(1)

    elif rc == 0:
        #Splits the command by spaces
        args = command.split()

        #Close stdout and duplicate to fd. Collaboration with Alan Uribe.
        if isPipe:
            os.close(r)
            fd = sys.stdout.fileno()
            os.dup2(w, fd)

        newArgs = []
        count = 1
        #Checks for redirection while keeping the arguments before the redirection
        for x in args:
            isRedir = x
            isRedir = isRedir[:2]
            if isRedir == ">":
                os.close(1)
                sys.stdout = open(args[count], "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                break
            elif isRedir == "<":
                with open(args[count], "r") as inRedir:
                    for line in inRedir:
                        line = line.strip()
                        newArgs.append(line)
                break
            else:
                #Stores the arguments before the redirection in a new list
                newArgs.append(args[count - 1])
                count += 1
        
        
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, newArgs, os.environ)
                for fd in (r, w):
                    os.close(fd)
                break
            except FileNotFoundError:
                pass

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)

    else:
        if isPipe:
            newArgs = []
            #Close stdin and duplicate with fd. Collaboration with Alan Uribe.
            os.close(w)
            fd = sys.stdin.fileno()
            os.dup2(r, fd)

            for line in fileinput.input():
                line = line.strip()
                newArgs.append(line)

            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, sCommand)
                try:
                    os.execve(program, newArgs, os.environ)
                    for f in (w, r):
                        os.close(f)
                    break
                except FileNotFoundError:
                    pass
        else:
            os.wait()
