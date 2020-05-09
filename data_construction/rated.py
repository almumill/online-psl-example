import pandas as pd

def to_one(x):
    return 1

def rated_predicate(observed_ratings_df, truth_ratings_df, setting='eval'):
    """
    Rated Predicates
    """
    observed_ratings_series = observed_ratings_df.loc[:, ['userId', 'movieId', 'rating']].set_index(
        ['userId', 'movieId'])

    truth_ratings_series = truth_ratings_df.loc[:, ['userId', 'movieId', 'rating']].set_index(
        ['userId', 'movieId'])

    # obs
    rated_series = pd.concat([observed_ratings_series, truth_ratings_series], join='outer')

    # this is a blocking predicate, so the observed values should all be 1s
    rated_series = rated_series['rating'].apply(to_one)

    rated_series.to_csv('../movielens/data/' + setting + '/rated_obs.txt',
                        sep='\t', header=False, index=True)
