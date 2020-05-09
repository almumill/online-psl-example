import pandas as pd


def avg_item_rating_predicate(observed_ratings_df, setting='eval'):
    """
    Average item rating predicate
    """
    observed_ratings_series = observed_ratings_df.loc[:, ['userId', 'movieId', 'rating']].set_index(
        ['userId', 'movieId'])
    filename = '../movielens/data/' + setting + '/avg_item_rating_obs.txt'
    handle = open(filename, "w")

    # reindex by movie ID so we can group them and calculate the mean easily
    observed_ratings_df = observed_ratings_df.reset_index()
    observed_ratings_df = observed_ratings_df.set_index('movieId')

    # calculate the mean within each movie
    for movieId in observed_ratings_df.index.unique():
        df_temp = observed_ratings_df[observed_ratings_df.index == movieId]
        item_avg = df_temp['rating'].mean()
        handle.write(str(movieId) + "\t" + str(item_avg) + "\n")
