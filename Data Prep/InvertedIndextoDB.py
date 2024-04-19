from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = 'mongodb+srv://usern:abcd1234@engine0001.vapavh9.mongodb.net/'
client = MongoClient(uri, server_api = ServerApi('1'))
f = open("InvertedIndex.txt", "r")
#635378
def pingM():
    try:
        client.admin.command('ping')
        print("You successfully connected!")
    except Exception as e:
        print(e)

def getCollection(dbname, collection):
   return client[dbname][collection]

def getInvertedIndex(file):
    InvertedIndex = []
    for line in file:
        InvertedIndex.append(line.split())
    return InvertedIndex

def main():
    pingM()
    Collection = getCollection("MovieInvertedIndex", "Iv-Id-m")
    Collection.delete_many({})
    InvInd = []
    for x in getInvertedIndex(f):
        t = []
        t.append(int(x[0]))
        t.append(x[1])
        t.append(int(x[2]))
        t2 = x[3].replace(',', ":").replace(')(', ",").replace("(", "").replace("\'", "").replace(")", "").split(',')
        t5 = []
        for x in t2:
            t3 = str(x).split(':')
            t4 = []
            for j in t3:
                t4.append(int(j))
            t5.append(t4)
        t.append(t5)
        InvInd.append(t)
    Collection.delete_many({})
    for x0 in InvInd:
       print(x0[0], x0[3])
       Collection.insert_one({"_id": x0[0], "keyWord": x0[1], "doc-Freq" : x0[2], "mList" : x0[3] })
    return 0

main()
print('OK 200')