import sys
import os
import math


# stopWordsList = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
# stopWordsDict = dict()
# for word in stopWordsList:
#     if word in stopWordsDict.keys():
#         continue
#     else:
#         stopWordsDict[word] = 1


modelDict = dict()

hamDocs = 0
spamDocs = 0

with open('nbmodelFinal.txt', 'r', encoding='latin1') as file:
    n = 0
    for line in file:
        if n == 0:
            lines = line.split( )
            hamDocs = int(lines[0])
            spamDocs = int(lines[1])
            n += 1
        else:
            eachDict = dict()
            wordList = line.split(' ')
            hamProb = wordList[1]
            spamProb = wordList[2]
            hamProb = hamProb.replace('\n', '')
            spamProb = spamProb.replace('\n', '')
            eachDict['ham'] = float(hamProb)
            eachDict['spam'] = float(spamProb)
            modelDict[wordList[0]] = eachDict
            # print(modelDict)

# devDirectory = sys.argv[1]
devDirectory = "C:/Users/navan/PycharmProjects/NLP_Assignment_1/dev/"

output = open('nboutputFinal.txt', "w")
wordProbabilityInClass = dict()
logProbabilityOfMessageInClass = dict()
bayesianProbabilityInClass = dict()
correctlyClassified = dict()
incorrectlyClassified = dict()

totalDocs = spamDocs + hamDocs

i = 0
docClass = ''
totalFiles = dict()
totalSpam = 0
totalHam = 0
for root, subdirs, files in os.walk(devDirectory):
    ham = 0
    spam = 0
    if len(subdirs) is 0:
        if 'ham' in root:
            docClass = 'ham'
        elif 'spam' in root:
            docClass = 'spam'
    for file in files:
        totalFiles[docClass] = len(files)

        for cl in eachDict.keys():
            logProbabilityOfMessageInClass[cl] = 0
            bayesianProbabilityInClass[cl] = 0

        fileName = os.path.join(root, file)
        f = open(fileName, "r", encoding="latin1")
        # print(fileName)
        for word in f.read().split( ):
            word = word.lower()
            # if word in stopWordsDict.keys():
            #     continue
            # print(word)
            if word in modelDict.keys():
                wordProbabilityInClass = modelDict[word]
                # print(wordProbabilityInClass)
                for cl in eachDict.keys():
                    logProbabilityOfMessageInClass[cl] += math.log(float(wordProbabilityInClass[cl]))
                    # print(logProbabilityOfMessageInClass)
                    # print(logProbabilityOfMessageInClass)

        bayesianProbabilityInClass['ham'] = math.log(hamDocs / totalDocs) + logProbabilityOfMessageInClass['ham']
        bayesianProbabilityInClass['spam'] = math.log(spamDocs / totalDocs) + logProbabilityOfMessageInClass['spam']
        if (bayesianProbabilityInClass['ham'] > bayesianProbabilityInClass['spam']):
            output.write('ham')
            output.write(' ')
            output.write(fileName)
            output.write('\n')
        else:
            output.write('spam')
            output.write(' ')
            output.write(fileName)
            output.write('\n')

#         if(bayesianProbabilityInClass['ham'] > bayesianProbabilityInClass['spam']):
#             ham += 1
#             totalHam += 1
#         else:
#             spam += 1
#             totalSpam += 1
#     if docClass == 'ham':
#         correctlyClassified[docClass] =  ham
#         incorrectlyClassified['spam'] = spam
#     elif docClass == 'spam':
#         correctlyClassified[docClass] = spam
#         incorrectlyClassified['ham'] = ham
# print(totalHam, totalSpam)
# print(correctlyClassified)
# print(incorrectlyClassified)
#
# accuracy = (correctlyClassified['spam'] + correctlyClassified['ham'])/(correctlyClassified['spam'] + correctlyClassified['ham'] + incorrectlyClassified['ham'] + incorrectlyClassified['spam'])
# precision = dict()
# recall = dict()
# fScore = dict()
# precision['spam'] = correctlyClassified['spam']/(correctlyClassified['spam'] + incorrectlyClassified['spam'])
# precision['ham'] = correctlyClassified['ham']/(correctlyClassified['ham'] + incorrectlyClassified['ham'])
# print(spamDocs, hamDocs)
# recall['spam'] = correctlyClassified['spam']/totalFiles['spam']
# recall['ham'] = correctlyClassified['ham']/totalFiles['ham']
# fScore['spam'] = (2*precision['spam']*recall['spam'])/(precision['spam']+recall['spam'])
# fScore['ham'] = (2*precision['ham']*recall['ham'])/(precision['ham']+recall['ham'])
#
# print(accuracy)
# print(precision)
# print(recall)
# print(fScore)
#
