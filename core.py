import requests


def GetMovies(j):
    MovieList = []
    for i in range(j):
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page="+ str(i) +"&sort_by=popularity.desc"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NjU4ZGZiYzJjZDgzNjA4YjIxYzA3MDYxNDYxYmRjZSIsInN1YiI6IjY1NDk3NDQwNmJlYWVhMDBlYWY5MjhhOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.pS55XJJ6tneqz7V8HLyKp94askJCWfMfdF8Fi2FsJ84"
        }

        response = requests.get(url, headers=headers)
        Movies = response.json()["results"]
        print(Movies)
        id = 0
        for movie in Movies:
            temp = []
            temp.append(id)
            temp.append(movie["title"])
            temp.append(movie["overview"])
            MovieList.append(temp)
        
        return MovieList

def WritetoText(f, List):
    for item in List:
            f.write(item[0] + " " + item[1] + " " + item[2] + "\n")
    return 0

def main():
    f = open("MovieList.txt", 'w')
    mList = GetMovies(2)
    WritetoText(f, mList)