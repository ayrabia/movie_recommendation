import pandas as pd

def find_by_title(df, query):
    result = df["title"].str.contains(query, case = False, na = False, regex = False)
    return df[result]

def movies_in_genre(df, genre):
    #takes the users query and lowercases it
    target = genre.lower()
    #use a lambda function to check for genre in genres
    result = df["genres"].apply(
        #ensures that genre is lowercase when called
        #checks if the user's word is in that list 
        lambda genres: target in [g.lower() for g in genres]
    )
    return df[result]


if __name__ == "__main__":
    from load_data import load_movies
    from queries import find_by_title, movies_in_genre

    df = load_movies()
    print(find_by_title(df, "knight"))
    print(movies_in_genre(df, "Animation"))