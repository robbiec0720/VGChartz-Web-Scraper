import time
import requests
import pandas as pd
from bs4 import BeautifulSoup, element

def get_all_data(filename):
    all_data = []
    game_list = open(filename, 'r')
    
    for game in game_list:
        all_data += get_game_data(game.strip())
        print(f'{game.strip()} Done')
            
    game_list.close()
    return all_data

def get_game_data(game_name):
    # link to search results
    url = f"https://www.vgchartz.com/games/games.php?name={game_name}&keyword=&console="
    url += "&region=All&developer=&publisher=&goty_year=&genre=&boxart=Both&banner=Both"
    url += "&ownership=Both&showmultiplat=Yes&results=50&order=TotalSales&showtotalsales=0&showtotalsales=1"
    url += "&showpublisher=0&showvgchartzscore=0&shownasales=0&shownasales=1&showdeveloper=0"
    url += "&showcriticscore=0&showpalsales=0&showpalsales=1&showreleasedate=0&showuserscore=0"
    url += "&showjapansales=0&showjapansales=1&showlastupdate=0&showothersales=0&showothersales=1"
    url += "&showshipped=0"
    
    # retry until successful
    while True:
        # retrieve webpage info
        search_results = requests.get(url)
        if search_results.status_code == 429:
            time.sleep(30)
            continue  
        elif search_results.status_code == 200:
            break
        
    # navigate to table
    soup = BeautifulSoup(search_results.text, 'lxml')
    table = soup.find('div', {'id': 'generalBody'})
    
    rows = table.find_all('tr')[3:-1]
    data = [] # stores data
    # get console list
    console_list = open('console_list.txt', 'r')
    consoles = [c.replace('\n', '') for c in console_list.readlines()]
    console_list.close()
    
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
    # retry until successful
    while True:
        # retrieve webpage info
        game_page = requests.get(link)
        if game_page.status_code == 429:
            time.sleep(30)
            continue
        elif game_page.status_code == 200:
            break
          
    # retrieve webpage info and navigate to game info section
    sub_soup = BeautifulSoup(game_page.text, 'lxml')
    gamebox = sub_soup.find('div', {'id': 'gameGenInfoBox'})
    h2s = gamebox.find_all('h2')
    
    # this info is not tagged so a manual search is necessary
    temp_tag = element.Tag
    for h2 in h2s:
        if h2.string == 'Genre':
            temp_tag = h2
    
    # returns the genre
    return temp_tag.next_sibling.string

print('*****Extracting Sales Data*****')
sales_data = get_all_data('game_list.txt')
sales_df = pd.DataFrame(sales_data, columns=['Title', 'Genre', 'Console', 'Total Sales', 'NA Sales', 'PAL Sales', 'Japan Sales', 'Other Sales'])
sales_df.to_csv('sales_data.csv', sep=',', index=False, encoding='utf-8')
print('******Extraction Finished******')
