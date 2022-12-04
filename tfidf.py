import math, re
from collections import Counter


# Remove all characters that are not words and whitespaces
def clean(text):
    cleaned = re.sub(r'http\S+', '', text)
    cleaned = re.sub('[^A-Za-z0-9_]+', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.lower().strip()

def lineReader(file):
    outputstrings = ""
    for x in file:
        outputstrings += x.rstrip('\n')
    return outputstrings

def remove_stopwords(val):
    global stopwords
    templist = val.split()
    for x in stopwords:
        templist = [i for i in templist if i != x]
    return templist


def remove_lemming(val):
    outputlist = []
    for x in val:
        if x.endswith('ing'):
            outputlist.append(x[:-3])
        elif x.endswith('ly'):
            outputlist.append(x[:-2])
        elif x.endswith('ment'):
            outputlist.append(x[:-4])
        else:
            outputlist.append(x)
    return outputlist


# preproc all files

stopwordsFile = open('stopwords.txt', 'r')
stopwords = stopwordsFile.read().splitlines()
inputFile = open('tfidf_docs.txt', 'r')
# format: name of file, preproc_name, tdidf_name, list of word frequencies, TD of each unique word (as a list), IDF of
# each word
outputFileNames = []
for line in inputFile:
    line = line.rstrip('\n')
    open_file = open(line, 'r')
    outputList = (remove_lemming(remove_stopwords(clean(lineReader(open_file)))))
    outputFileNames.append([line, "change_this_testing_preproc_" + line, 'change_this_tfidf_' + line, [], [], [], []])
    outputF = open("change_this_testing_preproc_" + line, 'w')
    outputString = ""
    for x in outputList:
        outputString = " ".join([outputString, x])
    outputF.write(outputString.strip())
    open_file.close()
    outputF.close()

# post proc and td-idf of files

# initial read through
countOfFiles = 0
for x in outputFileNames:
    wordcount = 0
    tdList = []
    f = open(x[1], 'r')
    counterList = Counter(f.readline().split()).most_common()
    outputFileNames[countOfFiles][3] = counterList
    for y in counterList:
        wordcount += y[1]
    for z in counterList:
        tdList.append((z[0], z[1] / wordcount))
    outputFileNames[countOfFiles][4] = tdList
    countOfFiles += 1

count = 0
for x in outputFileNames:
    idfList = []
    for y in outputFileNames[count][3]:
        countForWord = 0
        for z in range(countOfFiles):
            for a in outputFileNames[z][3]:
                if y[0] == a[0]:
                    countForWord += 1
        idfList.append((y[0], math.log(countOfFiles / countForWord) + 1))
    outputFileNames[count][5] = idfList
    count += 1

count = 0
for x in outputFileNames:
    tdidfList = []
    indexI = 0
    currentVal = outputFileNames[count][5]
    for y in outputFileNames[count][4]:
        tdidfList.append((y[0], round(float(y[1]) * float(currentVal[indexI][1]), 2)))
        indexI += 1
    outputFileNames[count][6] = tdidfList
    count += 1

count = 0
for x in outputFileNames:
    f = open(x[2], 'w')
    listSort = sorted(x[6], key=lambda y: (-(float(y[1])), y[0]), reverse=False)
    countedListSort = Counter(listSort).most_common(10)
    outList = []
    for y in countedListSort:
        outList.append(y[0])
    f.write(str(outList))