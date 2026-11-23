"""Suggests movies. Two baseline types (no ML yet):
- most_popular: for new users — best-rated movies with enough ratings.
- recommend_for_user: for known users — top movies in the genres
  they rate highly that they haven't seen yet (falls back to
  most_popular if we know too little about them)."""

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

def recommend_for_user(user_id, ratings, movies,k=10, min_genre_ratings = 3, top_genres = 2):
    #user's own ratings
    user_ratings = ratings[ratings["userId"] == user_id]
    #if there are no ratings, fall back to popularity
    if user_ratings.empty:
        return most_popular(ratings, movies, k=k)

    #rank all eligible movies globally before filtering for this user
    ranked = most_popular(
        ratings, movies, k = len(movies), min_ratings=10
    )
    #remove movies the user has already seen
    seen_ids = user_ratings["movieId"]
    unseen = ranked[~ranked["movieId"].isin(seen_ids)]

    #.epxlode() turns a movie with ["action", "comedy"] into two rows - one per genre
    movie_genres = movies[["movieId", "genres"]].explode("genres")

    user_genres = user_ratings.merge(movie_genres, on="movieId")

    #calculate user's average rating and rating count per genre
    genre_stats = user_genres.groupby("genres")['rating'].agg(
        avg = "mean",
        count = "count"
    )

    eligible_genres = genre_stats[
        genre_stats["count"] >= min_genre_ratings #3
    ]

    ranked_genres = eligible_genres.sort_values(
        ["avg", "count"], ascending = False
    )

    preferred_genres = ranked_genres.head(top_genres).index

    #if genre history is insufficient, fall back to unseen popular movies
    if preferred_genres.empty:
        return unseen.head(k).reset_index(drop = True)

    #find movies belonging to at least one preferred genre
    matching_movies = movie_genres[
        movie_genres["genres"].isin(preferred_genres)
    ]

    candidates = unseen[
        unseen["movieId"].isin(matching_movies["movieId"])
    ]

    if candidates.empty:
        return unseen.head(k).reset_index(drop = True)

    return candidates.head(k).reset_index(drop = True)


if __name__ == "__main__":
    import pandas as pd
    from load_data import load_movies, load_ratings

    # fake world: 5 Horror movies + 1 Drama, each with 10 "other people" ratings
    fake_movies = pd.DataFrame({
        "movieId": [1, 2, 3, 5, 6, 8],
        "title": ["H1", "H2", "H3", "H4", "H5", "D1"],
        "genres": [["Horror"], ["Horror"], ["Horror"], ["Horror"], ["Horror"], ["Drama"]],
    })
    rows = []
    for mid in [1, 2, 3, 5, 6, 8]:
        for u in range(100, 110):            # 10 ratings each → passes min_ratings=10
            rows.append((u, mid, 4.0, 0))
    # user 7: three Horror ratings, and ONE 5.0 Drama (the trap)
    rows += [(7, 1, 4.5, 0), (7, 2, 4.5, 0), (7, 3, 4.5, 0), (7, 8, 5.0, 0)]
    fake_ratings = pd.DataFrame(
        rows, columns=["userId", "movieId", "rating", "timestamp"]
    )

    # TEST 1 – the trap: D1's 5.0 must NOT win. User 7 saw H1-H3 and D1.
    r1 = recommend_for_user(7, fake_ratings, fake_movies)
    print("TEST 1 – user 7 (3 Horror ratings, one 5.0 Drama):")
    print(r1.to_string(index=False))
    assert set(r1["movieId"]) == {5, 6}, f"got {set(r1['movieId'])}, expected only unseen Horror"
    print("PASS")

    # TEST 2 – unknown user → popularity fallback, no crash
    r2 = recommend_for_user(999, fake_ratings, fake_movies)
    print("\nTEST 2 – unknown user 999:")
    print(r2.to_string(index=False))
    assert not r2.empty
    print("PASS")

    # TEST 3 – real data: must exclude movies user 1 already rated
    movies, ratings = load_movies(), load_ratings()
    r3 = recommend_for_user(1, ratings, movies)
    print("\nTEST 3 – real user 1:")
    print(r3.to_string(index=False))
    seen = set(ratings[ratings["userId"] == 1]["movieId"])
    assert not (set(r3["movieId"]) & seen), "recommended an already-rated movie!"
    print("PASS")

