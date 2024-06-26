from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import csv

#inintalize MongoDB database
uri = 'mongodb+srv://usern:abcd1234@engine0001.vapavh9.mongodb.net/'
client = MongoClient(uri, server_api = ServerApi('1'))
f = open("MovieList.csv", "r")

#Read in the text file
def readDoc(file):
    #O(n)
    #for storing each document
    csvreader = csv.reader(file)
    documents = []
    for line in csvreader:
        documents.append(line)
    return documents

#ping connection
def pingM():
    try:
        client.admin.command('ping')
        print("You successfully connected!")
    except Exception as e:
        print(e)

#get the cluster
def getCollection(dbname, collection):
   return client[dbname][collection]


def main():
    pingM()
    Collection = getCollection("MovieInvertedIndex", "MovieCollection")
    Collection.delete_many({})
    for line in readDoc(f):
        print(str(line[1]), str(line[2]))
        Collection.insert_one({"_id": int(line[0]), "title": str(line[1]), "poster-path" : str(line[2]), "summary" : str(line[3])})

    print("OK 200")
main()