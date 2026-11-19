import pandas as pd

def load_movies(path = "data/ml-latest-small/ml-latest-small/movies.csv"):
    df = pd.read_csv(path)
    #spli the genres on |
    df["genres"] = df["genres"].str.split("|")
    return df

def load_ratings(path ="data/ml-latest-small/ml-latest-small/ratings.csv"):
    df = pd.read_csv(path)
    return df



if __name__ == "__main__":
    df = load_movies()
    #print(df.head()) #returns the first 5 lines of the dataset
    #print(df.shape) #(rows, cols)
    #print(df.dtypes) # what type each column is
    print(df["genres"].isna().sum())
    print(df[df["genres"].isna()].head())
