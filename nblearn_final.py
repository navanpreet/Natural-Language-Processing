import os
import sys

rootDirectory = sys.argv[1]
# rootDirectory = "C:/Users/navan/PycharmProjects/NLP_Assignment_1/tenpercent/"


stopWordsList = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
stopWordsDict = dict()
for word in stopWordsList:
    if word in stopWordsDict.keys():
        continue
    else:
        stopWordsDict[word] = 1


global numOfFiles
global numOfFilesinClass
vocabulary = set()
totalNumberOfFilesinClass = dict()
totalNumberOfFiles = 0
wordOccurencesInClass = dict()
wordOccurencesInClass['spam'] = dict()
wordOccurencesInClass['ham'] = dict()


for root, subdirs, files in os.walk(rootDirectory):
    if len(subdirs) is 0:
        print(root)
        r = root.split("\\")
        print (r)
        documentClass = r[len(r)-1]
        documentCount = 0
        for file in files:
            documentCount += 1
            totalNumberOfFiles += 1
            if documentClass in totalNumberOfFilesinClass.keys():
                totalNumberOfFilesinClass[documentClass] += 1
            else:
                totalNumberOfFilesinClass[documentClass] = 1

            filePath = os.path.join(root, file)
            f = open(filePath, "r", encoding="latin1")
            for word in f.read().split():
                word = word.lower()
                if word in stopWordsDict.keys():
                    continue
                if word is not '':
                    vocabulary.add(word)
                    if  word in wordOccurencesInClass[documentClass].keys():
                        wordOccurencesInClass[documentClass][word] += 1
                    else:
                        wordOccurencesInClass[documentClass][word] = 1


file = open('nbmodelFinal.txt', 'w', encoding='latin1')
file.write(str(totalNumberOfFilesinClass['ham']))
file.write(' ')
file.write(str(totalNumberOfFilesinClass['spam']))
file.write('\n')

countInClass = dict()

for key in totalNumberOfFilesinClass.keys():
    countInClass[key] = dict()

print(countInClass.keys())

sizeOfVocabulary = len(vocabulary)
totalNumberOfWordsInClass = dict()
for cl in wordOccurencesInClass.keys():
    totalNumberOfWordsInClass[cl] = sum(wordOccurencesInClass[cl].values())

probabilityOfWordInClassWithSmoothing = dict()

for word in vocabulary:
    probabilityOfWordInClassWithSmoothing[word] = dict()
    for cl in countInClass.keys():
        if word not in wordOccurencesInClass[cl].keys():
            countInClass[cl][word] = 0
        elif word in wordOccurencesInClass[cl].keys():
            countInClass[cl][word] = wordOccurencesInClass[cl][word]
        probabilityOfWordInClassWithSmoothing[word][cl]  = (countInClass[cl][word] + 1)/(totalNumberOfWordsInClass[cl] + sizeOfVocabulary)
       
    file.write(word)
    file.write(' ')
    file.write(str(probabilityOfWordInClassWithSmoothing[word]['ham']))
    file.write(' ')
    file.write(str(probabilityOfWordInClassWithSmoothing[word]['spam']))
    file.write('\n')
