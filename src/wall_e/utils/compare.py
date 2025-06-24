def match_film(dico):
    dejavu = set()
    matched_film = {}
    for user in dico:
        for film in dico[user]:
            if (not(film in dejavu)):
                counter = success_film(film,dico)
                if counter["boole"]:
                    dejavu.add(film)
                    matched_film[film] ={"film":film,"count": counter["count"]}
    sorte = dict(sorted(matched_film.items(), key=lambda item: item[1]["count"], reverse=True))
    return sorte
    
def check_film_in_dico(title, lst):
    for film in lst:
        if film["title"] == title:
            return True
    return False

def success_film(film, dico):
    count = 0
    n = len(dico)
    for user in dico:
        if check_film_in_dico(film, dico[user]):
            count += 1
    return {"boole" :count > n/2, "count": count}