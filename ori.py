import requests
import nclib
import json

KEY = 'k_12345678'
SEARCH_API = 'https://imdb-api.com/en/API/SearchMovie/'
CAST_API = 'https://imdb-api.com/en/API/FullCast/'

def receive_data(connection):
    data = connection.recv(1).decode("utf-8")
    print(data, end="")
    return data

def parse_movie(current_movie_raw):
    movie = current_movie_raw[1:].rstrip()

    ret = (movie, date) = movie.split("(")
    ret[1] = ret[1][:-1]

    return ret

def get_movie_details(current_movie):
    data = parse_movie(current_movie) 
    
    def get_movie_id(data):
        url = SEARCH_API + KEY + '/' + data[0] + data[1]
        r = requests.get(url)
        
        ret = json.loads(r.text)["results"][0]["id"]
        return ret

    def get_movie_cast(id):
        url = CAST_API + KEY + '/' + id
        r = requests.get(url)
        j = json.loads(r.text)

        ret = []

        for num in range(0,5):
            ret.append(j["actors"][num]["name"])

        return ret

    id = get_movie_id(data)
    actors = get_movie_cast(id)

    return '; '.join(actors)

def send_movie_details(connection, details):
    connection.send(details)

def main():
    ADDRESS = 'challenge.ctf.games'
    PORT = 31260
    CURRENT_MOVIE = ""
    RECORD_MOVIE = False

    connection = nclib.Netcat((ADDRESS, PORT))
    
    while True:
        data = receive_data(connection)
        if RECORD_MOVIE:
            CURRENT_MOVIE += data
        if data == '>':
            RECORD_MOVIE = True
        if data == "\n" and RECORD_MOVIE:
            RECORD_MOVIE = False
            details = get_movie_details(CURRENT_MOVIE)
            print(details)
            send_movie_details(connection, str.encode(details))
            CURRENT_MOVIE = ""



if __name__ == '__main__':
    main()