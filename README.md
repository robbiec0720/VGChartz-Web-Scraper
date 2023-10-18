# VGChartz-Web-Scraper
A python script that scrapes sales data from the website vgchartz.com given a .txt file with a list of games. A single game may have multiple entries if it is on multiple platforms.

## generate_game_list.py
This script reads in the files 'genre_list.txt' and 'console_list.txt' which contain a list of genres and consoles respectively. The top 10 games with the most sales for each console-genre combination are extracted and stored in a new file 'game_list.txt'.