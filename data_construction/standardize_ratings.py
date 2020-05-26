import pandas as pd
# standardize ratings for each unique user


# convert the standard deviation score to a value in [0, 1]
def score_to_rating(score):
    if score > 2:
       score = 2
    elif score < -2:
       score = -2
    score += 3
    score = float(score / 5)
    return score

def standardize_user_ratings(df, id_col_name, rating_col_name, user_scaling_info = None):

    # to quickly access (user, movie) pairs we create a dictionary
    # that translates the pairs to the integer index in the dataframe

    rows = df.iterrows()
    user_movie_to_index = dict({})
    for row in rows:
       user_movie_to_index[(row[1]['userId'], row[1]['movieId'])] = row[0]
    print("created index dict")

    unique_users = df[id_col_name].unique()

    provided_scaling_info = (user_scaling_info is not None)

    if not provided_scaling_info:
        # store the mean/std for each user to standardize truth ratings
        user_scaling_info = dict({})

    for x in range(len(unique_users)):
        userId = unique_users[x]
        rating_count = df.loc[df['userId'] == userId].shape[0]
        print("did user " + str(x))
        print(rating_count)
        # don't standardize ratings when the user only contributed one
        if rating_count == 1:
            continue

        if not provided_scaling_info:
            user_avg = df.loc[df['userId'] == userId][rating_col_name].mean()
            user_std = df.loc[df['userId'] == userId][rating_col_name].std()
            user_scaling_info[userId] = [user_avg, user_std]
            print(user_std)

        # if we were provided info for standardizing truth ratings,
        # use that. If there's a user in truth who wasn't in obs,
        # set no_data to True and use it so we don't transform their ratings
        else:
            try:
                user_avg = user_scaling_info[userId][0]
                user_std = user_scaling_info[userId][1]
            except:
                user_std = 0
                user_avg = 0
                no_data = True

        # don't standardize ratings if they rate everything the same
        if user_std == 0:
            continue

        # get list of movies rated by user
        user_movie_list = df.loc[df['userId'] == userId]['movieId'].unique()
        for i in range(rating_count):
            cur_user = unique_users[x]
            cur_movie = user_movie_list[i]
            idx = user_movie_to_index[(unique_users[x], user_movie_list[i])]
            original_rating = df.at[idx, 'rating']
            original_rating -= user_avg
            original_rating /= user_std
            df.at[idx, 'rating'] = score_to_rating(original_rating)

    return df, user_scaling_info
