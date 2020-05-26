import numpy as np

# this function assumes we're taking in rows from user_df
# the columns are "movieId", "movie title", "release date", "video release date", "IMDb URL ", "unknown", "Action",
# "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
# "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"

def compare_vals(row1, row2):
    intersection_count = 0
    union_count = 0

    # column 6 is the first category, "Action"
    categories_start_idx = 6
    col_count = row1.size

    # count the number of categories they have in common
    for x in range(categories_start_idx, col_count):
        
        if row1[x] == 1 and row2[x] == 1:
            intersection_count += 1
        if row1[x] == 1 or row2[x] == 1:
            union_count += 1

    # avoid division by 0 if neither movie has a category for some reason
    if union_count == 0:
        union_count = 1

    return float(intersection_count / union_count)

# pass in the user info dataframe
def sim_content_items_predicate(movies_df, setting = 'eval'):
    """
    User similarity predicate
    """
    filename = "../movielens/data/" + setting + "/sim_content_items_obs.txt"
    handle = open(filename, "w")
    indices = movies_df.index
    # pairwise comparison of every user for now
    for x in range(len(indices)):
        x_similarities = []

        for y in range(len(indices)):
            x_similarities += [compare_vals(movies_df.iloc[x], movies_df.iloc[y])]

        # sort similarities and pick the block_size highest
        sims = np.argsort(x_similarities)
        sims = sims[::-1]
        for y in range(len(indices)):
            handle.write(str(indices[x]) + "\t" + str(indices[sims[y]]) + "\t" + str(x_similarities[sims[y]]) + "\n")
