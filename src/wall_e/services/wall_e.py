import requests
from bs4 import BeautifulSoup


def get_genre(list):
    name_list = ""
    for name in list:
        name_list += name + "+"
    return name_list[:-1]


def get_date(name):
    date = ""
    for char in name:
        if char in "0123456789":
            date += char
    return date


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
session = requests.Session()
session.headers.update(headers)


def scrap_watch_list(username, genre=[]):
    user_film = {}
    index = 1
    boucle = True
    url_start = f"https://letterboxd.com/{username}/watchlist/"
    genres = get_genre(genre)
    if (len(genre) > 0):
        url =  f"{url_start}/genre/{genres}/by/rating/page/"
    else:
        url = f"{url_start}by/rating/page/"
    print(url)
    films = []
    new_list = []
    print(index)
    while (boucle and index < 1000):
        response = session.get(url + str(index))

        # Vérifie si la requête s'est bien passée
        if response.status_code == 200:
            print("Page succefuly load !")
            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all("li", class_="griditem")
            if (len(quotes) == 0):
                boucle = False
            films = films + quotes
            index += 1

        else:
            print("Time out")
            boucle = False

    for film in films:
        title = film.find("img", class_="image").get("alt")
        new_list.append(title)
    user_film[username] = new_list

    return user_film[username]
