# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 14:50:11 2025

@author: arthu
"""

import requests
from bs4 import BeautifulSoup
import random
import time
from utilCompare import matchFilm

def getGenre(list):
    retour = ""
    for name in list:
        retour += name + "+"
    return retour[:-1]

def getDate(name):
    retour=""
    for char in name:
        if char in "0123456789":
            retour += char
    return retour


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
session = requests.Session()
session.headers.update(headers)



def ScrapWatchList(username, genres = []):
    userFilm = {}
    genre = genres
    index = 1
    boucle = True
    if (len(genre) > 0): 
        url = "https://letterboxd.com/" +username +"/watchlist/"+"genre/"+ getGenre(genre) +"/by/rating/page/"
    else :
        url ="https://letterboxd.com/" +username +"/watchlist/"+"by/rating/page/"
    print(url)
    films = []
    newList = []
    print(index)
    while (boucle and index < 1000):
        response = session.get(url + str(index))
    
        # Vérifie si la requête s'est bien passée
        if response.status_code == 200:
            print("Page chargée avec succès !")
            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all("li", class_="poster-container")
            if (len(quotes) ==0 ):
                boucle = False
            films =films + quotes
            index+=1
        
            
        else:
            print("t'es ban")
            boucle = False
        #time.sleep(random.uniform(0.5, 1))
        

    for film in films:
        title = film.find("img", class_="image").get("alt")
        #year = getDate(film.find("a", class_="frame has-menu").get("target-data-original-titel"))
        newList.append(title)
    userFilm[username] = newList
    
    
    return userFilm[username]


