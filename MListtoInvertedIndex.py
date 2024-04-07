import spacy
import timeit
import csv
#Using model to lemmatize words
np = spacy.load('en_core_web_sm')
#for reading files
f = open("MovieList.csv", "r")
#for writing tokens out
unigramfile = open("InvertedIndex.txt", "w")
#for writing words out
dict = open("dictionary.txt", "r")
writetodict = open("dictionary.txt", "w")
#start time
start = timeit.timeit()

def readDoc(f):
    #O(n)
    #for storing each document
    csvreader = csv.reader(f)
    documents = []
    for line in csvreader:
        documents.append(line)
    return documents

def CreateInvertedIndex(documents, docCount, wc):
    #for storing tokens
    worddict = {}
    #iterate all docs
    for document in documents:
        end = timeit.timeit()
        print(str(docCount) + " " + str(document[0]) + " " + str(end - start))
        #load model
        doc = np(document[2])

        #Get Doc Code
        #iterate all words in one doc
        for word in doc:
            #not punctiation and stop words and not numeric
            if(str(word) not in '.,;:\'\\n\"[]-()' and str(word).isalpha()):
                lemmaword = word.lemma_.lower()
                if(lemmaword not in worddict):
                    worddict[lemmaword] = [[wc, int(1), int(1)],[[document[0], int(1)]]]
                    wc+=1
                else:
                    #if its a new document then add 1 to document frequency
                    if(worddict[lemmaword][0][2] == 0):
                        worddict[lemmaword][0][1] += 1
                        worddict[lemmaword][0][2] = 1
                        worddict[lemmaword][1].append([document[0], int(1)])
                    else:
                        worddict[lemmaword][1][-1][1] += 1

        for token in worddict:
            worddict[token][0][2] = 0
        #start of New Doc
        docCount+=1
    return worddict

def Writeto(worddict, cdic):
    #get current dictionary
    diction = readDoc(cdic)
    #sort alphabetically
    myKeys = list(worddict.keys())
    myKeys.sort()
    sorted_dict = {i: worddict[i] for i in myKeys}

    for word in sorted_dict:
        if(not(word in diction)):
            writetodict.write(str(word) + "\n")

    #sort by global frequency
    sorted_dict2 = sorted(worddict.items(), key=lambda x:x[1][0])

    for sets in sorted_dict2:
        unigramfile.write(str(sets[1][0][0]) + " " + str(sets[0]) + " " + str(sets[1][0][1]) + " " + str(sets[1][1]).replace('[', '(').replace(']',')').replace('),' , ')')[1:-1].replace(" ", "") + "\n")

    unigramfile.close()
    writetodict.close()

def main():
    Writeto(CreateInvertedIndex(readDoc(f), 0, 0), dict)
    #runntime
    end = timeit.timeit()
    print('runntime: ' + str(end - start))
    print('Process Finished')
main()