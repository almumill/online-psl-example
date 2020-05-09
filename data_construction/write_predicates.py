import pandas as pd
import os
from ratings import ratings_predicate
from rated import rated_predicate
from sim_content_users import sim_content_users_predicate
from sim_content_items import sim_content_items_predicate
from avg_item_rating import avg_item_rating_predicate
from avg_user_rating import avg_user_rating_predicate
from user import user_predicate
from item import item_predicate
from sim_user import sim_users_predicate
from sim_items import sim_items_predicate

def construct_movielens_predicates():
    """
    :param books_df:
    :param interactions_df:
    :param reviews_df:
    :param obs_interactions:
    :param obs_reviews:
    :param target_interactions:
    :param target_reviews:
    :param truth_interactions:
    :param truth_reviews:
    :param setting:
    :return:
    """

    """
    Create data directory to write output to
    """
    if not os.path.exists('../movielens/data/eval/'):
        os.makedirs('../movielens/data/eval/')

    """
    Assuming that the raw data already exists in the data directory
    """
    movies_df, ratings_df, user_df = load_dataframes()
    movies_df, ratings_df, user_df = filter_dataframes(movies_df, ratings_df, user_df)
    # note that truth and target will have the same atoms
    observed_ratings_df, truth_ratings_df = partition_by_timestamp(ratings_df)

    users = ratings_df.userId.unique()
    movies = ratings_df.movieId.unique()

#    ratings_predicate(observed_ratings_df, truth_ratings_df)
#    rated_predicate(observed_ratings_df, truth_ratings_df)
    sim_content_users_predicate(user_df)
    sim_content_items_predicate(movies_df)
#    avg_item_rating_predicate(observed_ratings_df)
#    avg_user_rating_predicate(observed_ratings_df)
#    user_predicate(user_df)
#    item_predicate(movies_df)
#    sim_items_predicate(observed_ratings_df, truth_ratings_df, movies)
#    sim_users_predicate(observed_ratings_df, truth_ratings_df, users)

def partition_by_timestamp(ratings_df, train_proportion=0.8):
    sorted_frame = ratings_df.sort_values(by='timestamp')
    return (sorted_frame.iloc[: int(sorted_frame.shape[0] * train_proportion), :],
            sorted_frame.iloc[int(sorted_frame.shape[0] * train_proportion):, :])


def filter_dataframes(movies_df, ratings_df, user_df):
    """
    Get rid of users who have not yet rated more than n movies
    Note that there are no users where there are less than 20 ratings occurring in the raw datatset
    """
    return movies_df, ratings_df.groupby('userId').filter(lambda x: x.shape[0] > 5), user_df


def load_dataframes():
    """
    Assuming that the raw data already exists in the data directory
    """
    movies_df = pd.read_csv("../movielens/data/ml-100k/u.item", sep='|', header=None, encoding="ISO-8859-1")
    movies_df.columns = ["movieId", "movie title", "release date", "video release date", "IMDb URL ", "unknown", "Action",
                     "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                     "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    movies_df = movies_df.set_index('movieId')

    ratings_df = pd.read_csv('../movielens/data/ml-100k/u.data', sep='\t', header=None)
    ratings_df.columns = ['userId', 'movieId', 'rating', 'timestamp']
    ratings_df = ratings_df.astype({'userId': str, 'movieId': str})
    ratings_df.rating = ratings_df.rating / ratings_df.rating.max()

    user_df = pd.read_csv('../movielens/data/ml-100k/u.user', sep='|', header=None, encoding="ISO-8859-1")
    user_df.columns = ['userId', 'age', 'gender', 'occupation', 'zip']
    user_df = user_df.set_index('userId')

    return movies_df, ratings_df, user_df


def main():
    construct_movielens_predicates()


if __name__ == '__main__':
    main()
