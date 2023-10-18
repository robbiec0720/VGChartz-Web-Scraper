import requests
import pandas as pd
from bs4 import BeautifulSoup, element

def get_all_data(filename):
    all_data = []
    game_list = open(filename, 'r')
    for game in game_list:
        all_data += get_game_data(game.strip())
    game_list.close()
    return all_data

def get_game_data(game_name):
    # retrieve webpage info
    url = f"http://www.vgchartz.com/games/games.php?page=1&name={game_name}&order=TotalSales&ownership=Both&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=0&showdeveloper=0&showreleasedate=0&showlastupdate=0&showvgchartzscore=0&showcriticscore=0&showuserscore=0&showshipped=0&showmultiplat=Yes"
    search_results = requests.get(url)
    
    # navigate to table
    soup = BeautifulSoup(search_results.text, 'lxml')
    table = soup.find_all(id='generalBody')[0]
    rows = table.find_all('tr')[3:-1]
    
    data = [] # stores data
    consoles = ['PC', 'Xbox', 'X360', 'XOne', 'XSX', 'PS2', 'PS3', 'PS4', 'PS5', 'GCN', 'Wii', 'WiiU', 'NS']
    
    # get data from each row
    for row in rows:
        extracted_data = []
        row_data = row.find_all('td')
        
        # skips row if title does not match or the console is not in the pre-approved list
        if row_data[2].a.text.strip() != game_name or row_data[3].img.get('alt') not in consoles:
            continue
        
        extracted_data.append(row_data[2].a.text.strip()) # extracts title
        extracted_data.append(get_genre(row_data[2].a.get('href')))
        extracted_data.append(row_data[3].img.get('alt')) # extracts console
        extracted_data += [(n.string) for n in row_data[-5:]] # extracts sales numbers
        data.append(extracted_data)
    return data

def get_genre(link):
    # retrieve webpage info and navigate to game info section
    game_page = requests.get(link)
    sub_soup = BeautifulSoup(game_page.text, "lxml")
    gamebox = sub_soup.find("div", {"id": "gameGenInfoBox"})
    h2s = gamebox.find_all('h2')
    
    # this info is not tagged so a manual search is necessary
    temp_tag = element.Tag
    for h2 in h2s:
        if h2.string == 'Genre':
            temp_tag = h2
    
    # returns the genre
    return temp_tag.next_sibling.string

sales_data = get_all_data('game_list.txt')
sales_df = pd.DataFrame(sales_data, columns=['Title', 'Genre', 'Console', 'Total Sales', 'NA Sales', 'PAL Sales', 'Japan Sales', 'Other Sales'])
print(sales_df)