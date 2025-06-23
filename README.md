In order to use the scrapper yo need to download those following :

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
    
