

def build_user_vector(user_id, ratings, movies):
    #keep only ratings made by this user
    user_ratings = ratings[ratings["userId"] == user_id]

    #one row for each genre of each movie
    movie_genre = movies[["movieId", "genres"]].explode("genres")

    #attach the genres to the user's ratings using their shared movieId
    user_genres = user_ratings.merge(movie_genre, on = "movieId")

    #value has no usable genre information
    user_genres = user_genres[
        user_genres["genres"] != "(no genres listed)"
    ]

    #add up the users ratings within each genre
    user_vector = user_genres.groupby("genres")["rating"].sum()

    return user_vector

if __name__ == "__main__":
    from load_data import load_movies, load_ratings

    movies = load_movies()
    ratings = load_ratings()

    user_vector = build_user_vector(1, ratings, movies)
    print(user_vector)

