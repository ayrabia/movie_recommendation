

def most_popular(ratings, movies, k =10, min_ratings =10):

    #one row per movie: average rating + how many ratings
    stats = ratings.groupby("movieId")["rating"].agg(
        avg ="mean",
        count = "count"
    )

    #keep movies with enough ratings
    eligible = stats[stats["count"] >= min_ratings]

    #sort from highest average to lowest, then by rating count when averages are equal, then select k movies 
    ranked = eligible.sort_values(["avg", "count"], ascending = False)
    top_movies = ranked.head(k)

    #turn movieId from the index into a regular column
    top_movies = top_movies.reset_index()

    result = top_movies.merge(
        movies[["movieId", "title"]],
        on="movieId"
    )
    result["avg"] = result["avg"].round(2)
    return result[["movieId", "title", "avg", "count"]]
