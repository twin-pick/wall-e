# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 20:41:35 2025

@author: arthu
"""

def matchFilm(dico):
    dejavu = set()
    matchedFilm = {}
    for user in dico:
        for film in dico[user]:
            if (not(film in dejavu)):
                counter = successFilm(film,dico)
                if counter["boole"]:
                    dejavu.add(film)
                    matchedFilm[film] ={"film":film,"count": counter["count"]}
    sorte = dict(sorted(matchedFilm.items(), key=lambda item: item[1]["count"], reverse=True))
    return sorte
    
def checkFilmInDico(title, lst):
    for film in lst:
        if film["title"] == title:
            return True
    return False

def successFilm(film, dico):
    count = 0
    n = len(dico)
    for user in dico:
        if checkFilmInDico(film, dico[user]):
            count += 1
    return {"boole" :count > n/2, "count": count}