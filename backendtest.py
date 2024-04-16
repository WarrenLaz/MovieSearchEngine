from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import math

uri = 'mongodb+srv://usern:abcd1234@engine0001.vapavh9.mongodb.net/'
client = MongoClient(uri, server_api = ServerApi('1'))
swfile = open("stopwords.txt", "r")
#635378
def pingM():
    try:
        client.admin.command('ping')
        print("You successfully connected!")
    except Exception as e:
        print(e)

def getCollection(dbname, collection):
   return client[dbname][collection]

def Score(tf, N, df):
    return tf*math.log(N/df)

def similarity(A,B):
    sumdot = 0
    sumA = 0
    sumB = 0

    for i in range(len(A)):
        sumdot += A[i]*B[i]

    for i in range(len(A)):
        
        sumA += math.pow(A[i],2)

    for i in range(len(B)):
        sumB += math.pow(B[i],2)
    
    return sumdot/(math.sqrt(sumA)*math.sqrt(sumB))

def Freq(list):
    freq = {}
    for item in list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq

def getdocs(query1, dblist1):
    documents = []
    
    for word in query1:
        t = []
        wlist = dblist1.find_one({"keyWord" : word}) 
        t.append(word)
        t.append(wlist["doc-Freq"])
        t.append(wlist["mList"])
        documents.append(t)
        
    return documents
            


def main():
    pingM()
    dblist = getCollection("MovieInvertedIndex", "Iv-Id-m")
    inp = input("Query: ").lower()
    query = inp.split()
    ds = getdocs(query, dblist)
    l = 0
    for x in ds:
        print(x[1])
        l += x[1]
    for x in ds:
        print(math.log((1+l)/(x[1]+1)))





main()
    