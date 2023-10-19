# VGChartz-Web-Scraper
A Python script that scrapes sales data from the website vgchartz.com given a .txt file with a list of games. A single game may have multiple entries if it is on multiple platforms.

## generate_game_list.py
This script reads in the files 'genre_list.txt' and 'console_list.txt' which contain a list of genres and consoles respectively. The top 10 games with the most sales for each console-genre combination are extracted and stored in a new file 'game_list.txt'. \
_Note: The values in 'genre_list.txt' and 'console_list.txt' are found by inspecting the page source and they may differ from the text displayed on the webpage itself.__

## sales_scraper.py
This script reads in the file 'game_list.txt' and extracts information about those games and exports it into a new file 'sales_data.csv'. The information that is extracted includes the game's title, genre, console, total sales, NA sales, PAL sales, Japan sales, and other sales.
