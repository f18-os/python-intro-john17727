import re
import sys

inText = sys.argv[1]
outText = sys.argv[2]
wordList = []
allWords = {}

with open(inText, 'r') as inFile:
    #read each line in file
    for line in inFile:
        line = line.strip()
        #split line into the words
        aLine = re.split('[ \t]', line)
        for x in aLine:
            
            #get rid of punctuation
            if '."' in x:
                x = x[:-2] 
            if "." in x or "," in x or ";" in x or "!" in x or "?" in x or ":" in x:
                x = x[:-1]
            if '"' in x:
                x = x[1:]
            #lowercase everything
            x = x.lower()
            
            #special cases
            if "'" in x:
                aSplit = x.split("'")
                wordList.append(aSplit[0])
                wordList.append(aSplit[1])
            elif ".--" in x:
                dSplit = x.split('.--')
                wordList.append(dSplit[0])
                wordList.append(dSplit[1])
            elif "-" in x:
                hSplit = x.split('-')
                wordList.append(hSplit[0])
                wordList.append(hSplit[1])
            else:
                #if not empty string
                if x:
                    #build list
                    wordList.append(x)

#sort list
wordList.sort()

#insert the words in the list into a dictionary while simultaneously counting them
for y in wordList:
    if y in allWords:
        allWords[y] += 1
    else:
        allWords[y] = 1

outFile = open(outText, "w")
for z in allWords:
    outFile = open(outText, "a")
    outFile.write(z + " " + str(allWords[z]) + "\n")
outFile.close()
