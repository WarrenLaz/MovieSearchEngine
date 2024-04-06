import requests

def GetMovies(pages):
    MovieList = []
    id = 0
    for x in range(1, pages):
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page="+ str(x) +"&sort_by=popularity.desc"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NjU4ZGZiYzJjZDgzNjA4YjIxYzA3MDYxNDYxYmRjZSIsInN1YiI6IjY1NDk3NDQwNmJlYWVhMDBlYWY5MjhhOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.pS55XJJ6tneqz7V8HLyKp94askJCWfMfdF8Fi2FsJ84"
        }

        response = requests.get(url, headers=headers)
        Movies = response.json()["results"]
        
        for movie in Movies:
            temp = []
            temp.append(id)
            temp.append(movie["title"].replace(":", "").replace(",", ""))
            temp.append(movie["overview"].replace(",", "").replace("\n", " ").replace("\r", " "))
            MovieList.append(temp)
            print(str(id) + " " + temp[1])
            id += 1
    return MovieList

def WritetoText(f, List):
    for item in List:
        f.write(str(item[0]) + "," + item[1] + "," + item[2].rstrip() + "\n")
    f.close()
    return 0

def main():
    f = open("MovieList.csv", 'w')
    mList = GetMovies(500)
    WritetoText(f, mList)
main()