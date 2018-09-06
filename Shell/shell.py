
import os, sys, time, re

#Telling the user what to type to exit
print ("(Type Exit to quit.)")


while True: #keeps the program alive as long as user doesn't explicitly exit

    #Reads user inputs and commands
    os.write(1, ("PROMPT> ").encode())
    command = os.read(0, 50)

    #Checks if user typed exit
    isExit = command.decode()
    isExit = isExit[:4]
    isExit = isExit.lower()
    if isExit == "exit":
        sys.exit(1)
    

    rc = os.fork()

    if rc < 0:
        os.write(2, ("Failed. Now exiting.").encode())
        sys.exit(1)

    elif rc == 0:
        #Splits the command by spaces
        args = command.split()

        newArgs = []
        count = 1
        #Checks for redirection while keeping the arguments before the redirection
        for x in args:
            isRedir = x.decode()
            isRedir = isRedir[:2]
            if isRedir == ">":
                os.close(1)
                sys.stdout = open(args[count].decode(), "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                break
            else:
                #Stores the arguments before the redirection in a new list
                newArgs.append(args[count - 1])
                count += 1

        
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0].decode())
            try:
                os.execve(program, newArgs, os.environ)
                break
            except FileNotFoundError:
                pass

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)

    else:
        #Parent just waits :'(
        os.wait()