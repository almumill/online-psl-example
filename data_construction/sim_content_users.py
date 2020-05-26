import numpy as np

# this function assumes we're taking in rows from user_df
# the columns are 'age', 'gender', 'occupation', 'zip'
def compare_vals(row1, row2):
    bool_sum = 0

    # we disregard zip code
    if abs(row1['age'] - row2['age']) <= 10:
        bool_sum += 1
    if row1['gender'] == row2['gender']:
        bool_sum += 1
    if row1['occupation'] == row2['occupation']:
        bool_sum += 1

    return float(bool_sum / (row1.size - 1))

# pass in the user info dataframe
def sim_content_users_predicate(user_df, setting = 'eval'):
    """
    User similarity predicate
    """
    filename = "../movielens/data/" + setting + "/sim_content_users_obs.txt"
    handle = open(filename, "w")
    indices = user_df.index
    # pairwise comparison of every user for now
    for x in range(len(indices)):
        x_similarities = []

        for y in range(len(indices)):
            x_similarities += [compare_vals(user_df.iloc[x], user_df.iloc[y])]

        # sort similarities and pick the block_size highest
        sims = np.argsort(x_similarities)
        sims = sims[::-1]
        for y in range(len(indices)):
            handle.write(str(indices[x]) + "\t" + str(indices[sims[y]]) + "\t" + str(x_similarities[sims[y]]) + "\n")
