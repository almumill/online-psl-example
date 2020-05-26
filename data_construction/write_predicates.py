import pandas as pd
import os
import re
from timestamps import get_months_list, get_month_and_date, timestamp_matches_month
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
from standardize_ratings import standardize_user_ratings

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
    movies_df_dict, ratings_df_dict, user_df_dict, time_split_keys = split_by_months(movies_df, ratings_df, user_df)
    # note that truth and target will have the same atoms
    observed_ratings_df, truth_ratings_df = partition_by_timestamp(ratings_df)

    ordered_list_of_months = get_months_list(ratings_df)

    for i in range(len(ordered_list_of_months)):
        write_data_file(i)
        if not os.path.exists('../movielens/data/fold'+str(i)+'/'):
            os.makedirs('../movielens/data/fold'+str(i)+'/')
        # get observations/truths for this split
        ratings_df = ratings_df_dict[ordered_list_of_months[i]]
        observed_ratings_df, truth_ratings_df = partition_by_timestamp(ratings_df)
        user_df = user_df_dict[ordered_list_of_months[i]]
        movies_df = movies_df_dict[ordered_list_of_months[i]]

        observed_ratings_df, user_scaling_info = standardize_user_ratings(observed_ratings_df, 'userId', 'rating')
        truth_ratings_df, _ =  standardize_user_ratings(truth_ratings_df, 'userId', 'rating', user_scaling_info)
#
        users = ratings_df.userId.unique()
        movies = ratings_df.movieId.unique()

        ratings_predicate(observed_ratings_df, truth_ratings_df, setting = "fold"+str(i))
        rated_predicate(observed_ratings_df, truth_ratings_df, setting = "fold"+str(i))
#        sim_content_users_predicate(user_df, setting = "fold"+str(i))
#        sim_content_items_predicate(movies_df, setting = "fold"+str(i))
        avg_item_rating_predicate(observed_ratings_df, setting = "fold"+str(i))
        avg_user_rating_predicate(observed_ratings_df, setting = "fold"+str(i))
        user_predicate(user_df, setting = "fold"+str(i))
        item_predicate(movies_df, setting = "fold"+str(i))
        sim_items_predicate(observed_ratings_df, truth_ratings_df, movies, setting = "fold"+str(i))
        sim_users_predicate(observed_ratings_df, truth_ratings_df, users, setting = "fold"+str(i))
        print("Did split #"+str(i))
    for i in range(len(ordered_list_of_months)):
        print("Fold #"+str(i)+" -- " + str(ordered_list_of_months[i]))

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

def write_data_file(i):
    filename = "../movielens/cli/movielens-fold"+str(i)+".data"
    datafile = """
predicates:
    rated/2: closed
    rating/2: open
    sim_items/2: closed
    sim_users/2: closed
    user/1: closed
    item/1: closed
    avg_item_rating/1: closed
    avg_user_rating/1: closed
    sim_content_items/2: closed
    sim_content_users/2: closed

observations:
    rated: ../data/foldk/rated_obs.txt
    rating: ../data/foldk/rating_obs.txt
    sim_items: ../data/foldk/sim_cosine_items_obs.txt
    sim_users: ../data/foldk/sim_cosine_users_obs.txt
    user: ../data/foldk/user_obs.txt
    item: ../data/foldk/item_obs.txt
    avg_item_rating: ../data/foldk/avg_item_rating_obs.txt
    avg_user_rating: ../data/foldk/avg_user_rating_obs.txt
    sim_content_items: ../data/foldk/sim_content_items_obs.txt
    sim_content_users: ../data/foldk/sim_content_users_obs.txt

targets:
    rating: ../data/foldk/rating_targets.txt

truth:
    rating: ../data/foldk/rating_truth.txt
    """
    datafile = re.sub("foldk", "fold"+str(i), datafile)
    open(filename, "w").write(datafile)

def split_by_months(movies_df, ratings_df, users_df):
    """
    return a list of dataframes,
    movies/ratings/users for each month
    """

    year_month_tuples = get_months_list(ratings_df)

    movies_df_dict = dict({})
    ratings_df_dict = dict({})
    users_df_dict = dict({})

    for time_tuple in year_month_tuples:
        ratings_df_temp = ratings_df.loc[timestamp_matches_month(ratings_df, time_tuple)]

        # get user/item dfs with only users/items
        # that actually show up in the data
        user_list = [int(x) for x in ratings_df_temp['userId'].unique()]
        item_list = [int(x) for x in ratings_df_temp['movieId'].unique()]

        users_df_temp = users_df.loc[user_list]
        movies_df_temp = movies_df.loc[item_list]
        print(users_df_temp.shape[0])

        movies_df_dict[time_tuple] = movies_df_temp
        ratings_df_dict[time_tuple] =  ratings_df_temp
        users_df_dict[time_tuple] =  users_df_temp

    return movies_df_dict, ratings_df_dict, users_df_dict, year_month_tuples

def main():
    construct_movielens_predicates()


if __name__ == '__main__':
    main()
