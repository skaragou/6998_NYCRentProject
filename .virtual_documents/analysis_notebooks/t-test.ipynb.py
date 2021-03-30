import pandas as pd
import numpy as np
import statsmodels.stats as sm
import seaborn as sns
import matplotlib.pyplot as plt
import ast
import re


df = pd.read_csv("data/apartment_data_compiled.csv") 


# Get all amenities  
cols = set()
df['amenities'].apply(lambda x: [cols.add(i) for i in ast.literal_eval(x)])


amenity_list = dict()

for amenity in cols:
    amenity_list[amenity] = []


for _, row in df.iterrows():
    amenities =  ast.literal_eval(row['amenities'])
    for amenity in cols:
        if amenity in amenities:
            amenity_list[amenity].append(1)
        else:
            amenity_list[amenity].append(0)


df2 = pd.DataFrame(amenity_list)


new_df = df.join(df2)


new_df


df['rent_price'] = df['rent_price'].apply(lambda x: re.sub("[^0-9]", "", x)).astype(int)


df['has_amenity'] = np.any(df2,axis=1)


df.groupby(['BIN','apt_num']).agg({'has_amenity': np.mean})['has_amenity'].value_counts()


rent_prices = df.groupby(['BIN','apt_num']).agg({'rent_price': np.mean})['rent_price'].values


has_amenity = df.groupby(['BIN','apt_num']).agg({'has_amenity': np.mean})['has_amenity'].values


x1 = rent_prices[has_amenity == 0]
x2 = rent_prices[has_amenity == 1]


sm.weightstats.ttest_ind(x1,x2,'smaller')



