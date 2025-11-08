import pandas as pd

def preprocess(df, region_df):
    # Filter Summer Olympics only
    df = df[df['Season'] == "Summer"]

    # Merge region dataframe for region names
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicates safely
    df.drop_duplicates(inplace=True)

    # One-hot encoding of medals to separate columns
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
