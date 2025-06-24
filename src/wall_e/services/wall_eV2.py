from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import re


from compare import match_film  # tu le gardes si tu l’utilises plus tard

def get_genre(liste):
    return "+".join(liste)



def scrap_watch_list(username, genres=[]):
    user_film = {}
    genre = genres
    index = 1
    films = []
    boucle = True


    if genre:
        url = f"https://letterboxd.com/{username}/watchlist/genre/{get_genre(genre)}/by/rating/page/"
    else:
        url = f"https://letterboxd.com/{username}/watchlist/by/rating/page/"
    
    print("URL:", url)

    # Configuration de Selenium (headless facultatif)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        while boucle and index < 1000:
            print(f"Chargement de la page {index}")
            driver.get(url + str(index))
            time.sleep(random.uniform(0.1, 0.15))  # attendre un peu que la page charge

            # Utiliser BeautifulSoup sur la source HTML complète
            soup = BeautifulSoup(driver.page_source, "html.parser")

            quotes = soup.find_all("li", class_="poster-container")
            
            if not quotes:
                print("Aucun film trouvé sur cette page.")
                boucle = False
            else:
                films += quotes
                index += 1

    finally:
        driver.quit()

    new_list = []
    for film in films:
        span = film.find("span", class_="frame-title")
        if span:
            value = span.get_text()
            match = re.match(r"^(.*)\s\((\d{4})\)$", value)
            
            if match:
                nom = match.group(1)
                date = match.group(2)
                new_list.append({"title": nom, "date": date})

    user_film[username] = new_list
    return user_film[username]

