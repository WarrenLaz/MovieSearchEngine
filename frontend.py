import tkinter as tk
from tkinter import Text, ttk
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from PIL import ImageTk, Image
from urllib.request import urlopen
import io
import math
import spacy

np = spacy.load('en_core_web_sm')

uri = 'mongodb+srv://usern:abcd1234@engine0001.vapavh9.mongodb.net/'
client = MongoClient(uri, server_api = ServerApi('1'))
#["MovieInvertedIndex"]["MovieCollection"]
window = tk.Tk()
window.geometry('1000x1000')
window.title('Movie Search')
custom_font1 = ("Helvetica", 30)
custom_font2 = ("Helvetica", 20)
custom_font3 = ("Helvetica", 10)
MovieDatab = client["MovieInvertedIndex"]["MovieCollection"]
Invidx = client["MovieInvertedIndex"]["Iv-Id-m"]

def pingM():
    try:
        client.admin.command('ping')
        print("You successfully connected!")
    except Exception as e:
        print(e)

def Score(tf, N, df):
    return tf*math.log((N/df))

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

def getDocs(qu):
    wordlist = []
    for x in qu:
        print(x)
        m = Invidx.find_one({"keyWord" : x})
        if(m != None):
            wordlist.append(m['mList'])
    return wordlist


def GetMovie():
    query = str(np(text_box.get('1.0', 'end').replace("\n", "").replace("\r", "").lower())).split()

    queryF = Freq(query)
    docs = getDocs(queryF)
    #tf*math.log(N/df) (tf, N, df)
    queryvector = []
    i = 0

    for words in docs:
        queryvector.append(Score(queryF[query[i]]/len(query), 635378,len(words)+1))
        i+=1

    DocVectors = {}
    j = 0
    for words in docs:

        for movies in words:
            print(movies)
            if movies[0] in DocVectors :
                DocVectors[movies[0]][j] += Score(movies[1]/movies[2],635378,len(words)+1)
                print(j, DocVectors[movies[0]][j])
            else:
                v = []
                for i in range(len(queryvector)):
                    v.append(0)
                
                v[j] += Score(movies[1]/movies[2],635378,len(words)+1)
                DocVectors[movies[0]] = v
                print(j, DocVectors[movies[0]][j])
        j+=1
    scores = []

    #print(queryvector)

    for docs in DocVectors:
        print(docs, DocVectors[docs])
        scores.append([docs,similarity(queryvector,DocVectors[docs])])
    scores.sort(key= lambda x: x[1])

    rmovies = []

    for i in range(4):
        a = i * -1
        rmovies.append(scores[a][0])
    get_value(rmovies)



def get_value(movie):
    for m in movie:
        # Retrieve the value from the text box
        title = MovieDatab.find_one({"_id" : int(m)})['title']
        summary = MovieDatab.find_one({"_id" : int(m)})['summary']

        labelmovie = tk.Label(window, text = title, font=custom_font2)
        labelmovie.pack(padx=10, pady=10)
        Tx = Text(window, height = 10, width = 80)
        Tx.pack()
        Tx.insert(tk.END, summary)
        labelmovie.config(text=title)
    print('done')

pingM()

label = tk.Label(window, text = 'MOVIE SEARCH', font=custom_font1)
label.pack(padx=10, pady=10)
text_box = tk.Text(window, height=2, width=50)
text_box.pack(padx=10, pady=10)
button = tk.Button(window, text="Enter", command=GetMovie)
button.pack(padx=10, pady=5)
# run
window.mainloop()
