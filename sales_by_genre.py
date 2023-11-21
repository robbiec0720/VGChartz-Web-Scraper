import numpy as np
import pandas as pd

# get console, genre, and sales data
sales_df = pd.read_csv('sales_data_clean.csv')
consoles = sorted(list(set(sales_df['Console'])))
genres = sorted(list(set(sales_df['Genre'])))

# get total sales data by console and genre
sales_col = ['Total Sales', 'NA Sales', 'PAL Sales', 'Japan Sales', 'Other Sales']
sales_by_genre_data = []
for c in consoles:
    for g in genres:
        row_data = [c, g]
        for col in sales_col:
            row_data.append(sales_df[(sales_df['Console'] == c) & (sales_df['Genre'] == g)][col].sum().round(2))
        sales_by_genre_data.append(row_data)
        
sales_by_genre_df = pd.DataFrame(sales_by_genre_data, columns=['Console', 'Genre']+sales_col)
sales_by_genre_df.to_csv('sales_by_genre.csv', sep=',', index=False, encoding='utf-8')
