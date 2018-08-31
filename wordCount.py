import re
import sys

inText = sys.argv[1]
outText = sys.argv[2]
wordList = []
allWords = {}

#remove punctuation
def remPunc(aWord):
    while "." in aWord or "," in aWord or ";" in aWord or "!" in aWord or "?" in aWord or ":" in aWord or "-" in aWord or '"' in aWord:
        #checks for punctuations in front of word
        if "." in aWord[:1] or "," in aWord[:1] or ";" in aWord[:1] or "!" in aWord[:1] or "?" in aWord[:1] or ":" in aWord[:1] or "-" in aWord[:1] or '"' in aWord[:1]:
            aWord = aWord[1:]
        #checks for punctuations at the end of word
        if "." in aWord[-1:] or "," in aWord[-1:] or ";" in aWord[-1:] or "!" in aWord[-1:] or "?" in aWord[-1:] or ":" in aWord[-1:] or "-" in aWord[-1:] or '"' in aWord[-1:]:
            aWord = aWord[:-1]
    return aWord

with open(inText, 'r') as inFile:
    #read each line in file
    for line in inFile:
        line = line.strip()
        #split line into the words
        aLine = re.split('[ \t]', line)
        for x in aLine:
            x = x.lower()
            #split words with a hyphen
            if "-" in x:
                hyphenSplit = x.split("-")
                x = remPunc(hyphenSplit[0])
                wordList.append(x)
                x = remPunc(hyphenSplit[-1])
                wordList.append(x)
            #split words with a apostrophe
            elif "'" in x:
                aposSplit = x.split("'")
                x = remPunc(aposSplit[0])
                wordList.append(x)
                x = remPunc(aposSplit[-1])
                wordList.append(x)
            else:
                #if not empty string
                if x:
                    x = remPunc(x)
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
