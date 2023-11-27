import numpy as np
import pandas as pd


def get_title_sales(df, title):
    return df.loc[df['Title'] == title]

# get console, genre, and sales data
sales_df = pd.read_csv('sales_data_clean.csv')
generations = sorted(list(set(sales_df['Generation'])))
genres = sorted(list(set(sales_df['Genre'])))

# sort by total sales
sales_df = sales_df.sort_values('Total Sales', ascending=False)

# get top 10 games per generation and genre
top_10_data = []
for gen in generations:
    for g in genres:
        top_10 = sales_df[(sales_df['Generation'] == gen) & (sales_df['Genre'] == g) & (sales_df['Total Sales'] > 0)]
        
        # extraction helpers
        names = set()
        i = 0
        while len(names) < 10 and i < len(top_10):
            if(len(names) != (names.add(top_10.iloc[i]['Title']) or len(names))):
                title_df = get_title_sales(top_10, top_10.iloc[i]['Title']).to_numpy()
                for row in title_df:
                    top_10_data.append(row)
            i += 1

top_10_df = pd.DataFrame(top_10_data, columns=sales_df.columns)
top_10_df = top_10_df.sort_values('Total Sales', ascending=False)
top_10_df.to_csv('top_10_sales.csv', sep=',', index=False, encoding='utf-8')