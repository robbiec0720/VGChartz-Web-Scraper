import numpy as np
import pandas as pd

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
        top_10 = sales_df[(sales_df['Generation'] == gen) & (sales_df['Genre'] == g) & (sales_df['Total Sales'] > 0)].to_numpy()
        for i in range(10):
            if i < len(top_10):
                top_10_data.append(top_10[i])

top_10_df = pd.DataFrame(top_10_data, columns=sales_df.columns)
top_10_df = top_10_df.sort_values('Total Sales', ascending=False)
top_10_df.to_csv('top_10_sales.csv', sep=',', index=False, encoding='utf-8')
