import numpy as np
import pandas as pd

# get console and genre data
console_list = open('console_list.txt', 'r')
consoles = [c.replace('\n', '') for c in console_list.readlines()]
console_list.close()

genre_list = open('genre_list.txt', 'r')
genres = [g.replace('\n', '') for g in genre_list.readlines()]
genre_list.close()

sales_df = pd.read_csv('sales_data.csv')
sales_df = sales_df.fillna('0.0m') # replace NA with 0.0m

# remove 'm' from sales data
sales_col = ['Total Sales', 'NA Sales', 'PAL Sales', 'Japan Sales', 'Other Sales']
for col in sales_col:
    sales_df[col] = sales_df[col].map(lambda s: float(s[:-1]))

# get total sales data by console and genre
sales_by_genre_data = []
for c in consoles:
    for g in genres:
        row_data = [c, g.replace('+', ' ')]
        for col in sales_col:
            row_data.append(sales_df[(sales_df['Console'] == c) & (sales_df['Genre'] == g)][col].sum().round(2))
        sales_by_genre_data.append(row_data)
        
sales_by_genre_df = pd.DataFrame(sales_by_genre_data, columns=['Console', 'Genre']+sales_col)
sales_by_genre_df.to_csv('sales_by_genre.csv', sep=',', index=False, encoding='utf-8')
# sales_by_genre = sales_by_genre_df[sales_by_genre_df['Total Sales'] > 0.0]
