def user_predicate(user_df, setting = 'eval'):
    filename = "../movielens/data/" + setting + "/user_obs.txt"
    handle = open(filename, "w")
    for userId in user_df.index:
        handle.write(str(userId) + "\t1\n")
