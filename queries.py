import pandas as pd

def find_by_title(df, query):
    mask = df["title"].str.contains(query, case = False, na = False, regex = False)
    return df[mask]

def movies_in_genre(df, genre):
    #use a lambda function to check for genre in genres
    mask = df["genres"].apply(lambda genres: genre in genres)
    return df[mask]


if __name__ == "__main__":
    from load_data import load_movies
    from queries import find_by_title, movies_in_genre

    df = load_movies()
    print(find_by_title(df, "knight"))
    print(movies_in_genre(df, "Animation"))