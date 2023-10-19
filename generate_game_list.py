import time
import requests
from bs4 import BeautifulSoup

# get console and genre data
console_list = open('console_list.txt', 'r')
consoles = [c.replace('\n', '') for c in console_list.readlines()]
console_list.close()

genre_list = open('genre_list.txt', 'r')
genres = [g.replace('\n', '') for g in genre_list.readlines()]
genre_list.close()

# store game titles in a set so there are no duplicates
game_titles = set()
games_per_genre = 10 # this value can be to 10, 25, 50, 100, or 200

print('*****Generating Game List*****')

for console in consoles:
    for genre in genres:
        # retrieve webpage info
        url = f"https://www.vgchartz.com/games/games.php?name=&keyword=&console={console.strip()}"
        url += f"&region=All&developer=&publisher=&goty_year=&genre={genre.strip()}&boxart=Both&banner=Both"
        url += f"&ownership=Both&showmultiplat=Yes&results={games_per_genre}&order=TotalSales&showtotalsales=0&showtotalsales=1"
        url += "&showpublisher=0&showvgchartzscore=0&shownasales=0&shownasales=1&showdeveloper=0"
        url += "&showcriticscore=0&showpalsales=0&showpalsales=1&showreleasedate=0&showuserscore=0"
        url += "&showjapansales=0&showjapansales=1&showlastupdate=0&showothersales=0&showothersales=1"
        url += "&showshipped=0"
        search_results = requests.get(url)
            
        # navigate to table
        soup = BeautifulSoup(search_results.text, 'lxml')
        #print(soup.find_all(id='generalBody'))
        table = soup.find('div', {'id': 'generalBody'})
        rows = table.find_all('tr')[3:-1]
        
        # get games from list
        for row in rows:
            row_data = row.find_all('td')
            game_titles.add(row_data[2].a.text.strip())
        
        print(f'{console} {genre} Done')
    # sleep to avoid too many concurrent requests
    time.sleep(30)
            
# add titles to game list
game_list = open('game_list.txt', 'w', encoding='utf-8')

for title in game_titles:
    game_list.write(title + '\n')

game_list.close()
print('*****Generation Completed*****')
