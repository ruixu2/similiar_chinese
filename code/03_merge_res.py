import os
import pandas as pd

item_list = os.listdir("../similar/")
df_list = []
print(len(item_list))
for item in item_list:
    df = pd.read_csv(f"../similar/{item}")
    for i in range(df.shape[0]):
        df.loc[i, 'code1'] = ord(df.loc[i, 'char1'])
        df.loc[i, 'code2'] = ord(df.loc[i, 'char2'])
    df_list.append(df)
all_df = pd.concat(df_list)
all_df['code1'] = all_df['code1'].astype(int)
all_df['code2'] = all_df['code2'].astype(int)
all_df.to_csv("../result/similar.csv", index=False)
