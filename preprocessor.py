import pandas as pd


def preprocess(df,region_df):
    #filter summer olymnpics
    df = df[df['Season'] == "Summer"]
    # merge region df
    df = df.merge(region_df, on='NOC',how='left')
    # drop duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding
    df= pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df