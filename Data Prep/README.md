## Dependencies
MongoDB Atlas: python -m pip install "pymongo[srv]" \
Request: pip install request \
Spacey: pip install spacey 

## Code
<ins>TMDBtoTxt.py</ins> : This takes the TMDB website and scrapes all movies within 500 pages totaling the movies within our database to 10,000. There are more than 100,000 movies so this may not result in the best results. \
<ins>MListtoInvertedIndex.py</ins> : This converts the text file into an inverted index with each movies key being in place to reference the film.\
<ins>MDBMongo.py</ins> : This transfers the data written to the text file into a mongoDB cluster where each document represents a movie with the JSON structure as follows {_id:int,title:string,summary:string}. \
<ins>InvertedIndextoDB.py</ins> : This transfers the invertedIndex.txt into a mongoDB cluster where each document represents a word within the dictionary. This JSON structure is as follows: {_id:int,keyword:string,doc-Freq:int,mList:Array()}

