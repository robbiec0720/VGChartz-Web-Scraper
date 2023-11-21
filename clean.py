import pandas as pd

def console_to_generation(console):
    if console in ['GameCube', 'PlayStation2', 'Xbox']:
        return 6
    elif console in ['Wii', 'PlayStation 3', 'Xbox 360']:
        return 7
    elif console in ['Wii U', 'PlayStation 4', 'Xbox One']:
        return 8
    return -1

sales_df = pd.read_csv('sales_data_raw.csv')
sales_df = sales_df.fillna('0.0m') # replace NA with 0.0m

# mapping console abbreviations to full names
console_names = {'GC' : 'GameCube',
                 'PS2' : 'PlayStation 2',
                 'XB' : 'Xbox',
                 'Wii' : 'Wii',
                 'PS3' : 'PlayStation 3',
                 'X360' : 'Xbox 360',
                 'WiiU' : 'Wii U',
                 'PS4' : 'PlayStation 4',
                 'XOne' : 'Xbox One'}
sales_df['Console'] = sales_df['Console'].map(lambda c: console_names[c])

# remove 'm' from sales data
sales_col = ['Total Sales', 'NA Sales', 'PAL Sales', 'Japan Sales', 'Other Sales']
for col in sales_col:
    sales_df[col] = sales_df[col].map(lambda s: float(s[:-1]) if type(s) == str else s)
    
# add generation col
sales_df['Generation'] = sales_df['Console'].map(console_to_generation)
    
sales_df.to_csv('sales_data_clean.csv', sep=',', index=False, encoding='utf-8')
