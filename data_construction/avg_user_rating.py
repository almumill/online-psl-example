import pandas as pd


def avg_user_rating_predicate(observed_ratings_df, setting='eval'):
    """
    Average user rating predicate
    """
    observed_ratings_series = observed_ratings_df.loc[:, ['userId', 'movieId', 'rating']].set_index(
        ['userId', 'movieId'])
    filename = '../movielens/data/' + setting + '/avg_user_rating_obs.txt'
    handle = open(filename, "w")

    # reindex by movie ID so we can group them and calculate the mean easily
    observed_ratings_df = observed_ratings_df.reset_index()
    observed_ratings_df = observed_ratings_df.set_index('userId')

    # calculate the mean within each movie
    for userId in observed_ratings_df.index.unique():
        df_temp = observed_ratings_df[observed_ratings_df.index == userId]
        user_avg = df_temp['rating'].mean()
        handle.write(str(userId) + "\t" + str(user_avg) + "\n")
