In order to use the scrapper (V1) yo need to download those following :

        pip install requests beautifulsoup4 

then use the function scrapWathcList in the file walle/wall-e.py. 
function wich require two arguments :
    usernames : list of string, the name of the letterboxd account (name displayed in the url of the website not displayed on their page)
    genres : list of string, the different genre for the research (no capital letters)

the output of the function is a json objet like this :
    
    {
      <movie's name> : {
          film : {
            title : <movie's name>
            imageLink : <url to the letterboxd poster>
          }
          count : <int> (the number of user who have the movie in their watchlist)
      }
    }

sorted in descending order of the count key

To use the V2 of the scrapper, download the following:

        pip install selenium beautifulsoup4

input : username : string, genres : [string] (optional)
output : [{
        title : string,
        date: string,
        }]

exemple : 

scrapWatchList("66Sceptre", ["horror"]) => [{'title': 'The Thing', 'date': '1982'}, {'title': 'Psycho', 'date': '1960'}, {'title': 'Possession', 'date': '1981'}, {'title': 'The Lighthouse', 'date': '2019'}, {'title': 'Train to Busan', 'date': '2016'}, {'title': 'Invasion of the Body Snatchers', 'date': '1978'}, {'title': 'Suspiria', 'date': '1977'}, {'title': 'Funny Games', 'date': '1997'}, {'title': 'Videodrome', 'date': '1983'}, {'title': 'Carrie', 'date': '1976'}, {'title': 'American Psycho', 'date': '2000'}, {'title': 'The Others', 'date': '2001'}, {'title': 'Portrait of God', 'date': '2022'}, {'title': 'A Tale of Two Sisters', 'date': '2003'}, {'title': 'Under the Skin', 'date': '2013'}, {'title': 'Annihilation', 'date': '2018'}, {'title': 'The Lost Films of Bloody Nora', 'date': '2019'}, {'title': 'I Saw the TV Glow', 'date': '2024'}, {'title': 'X', 'date': '2022'}, {'title': 'Constantine', 'date': '2005'}, {'title': 'The Cabin in the Woods', 'date': '2011'}, {'title': 'Lake Mungo', 'date': '2008'}, {'title': 'Triangle', 'date': '2009'}, {'title': 'Brotherhood of the Wolf', 'date': '2001'}, {'title': "Gerald's Game", 'date': '2017'}, {'title': 'Life', 'date': '2017'}, {'title': 'Cuckoo', 'date': '2024'}, {'title': 'Azrael', 'date': '2024'}, {'title': 'Van Helsing', 'date': '2004'}, {'title': 'Lovely, Dark, and Deep', 'date': '2023'}, {'title': "Don't Move", 'date': '2024'}, {'title': 'You Should Have Left', 'date': '2020'}]
