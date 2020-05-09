def item_predicate(movies_df, setting = 'eval'):
    filename = "../movielens/data/" + setting + "/item_obs.txt"
    handle = open(filename, "w")
    for movieId in movies_df.index:
        handle.write(str(movieId) + "\t1\n")
