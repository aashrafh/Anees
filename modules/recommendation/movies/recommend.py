# %%
import dill as pickle
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# %% [markdown]
# # Prepare data

# %%
data_path = "../Data/ml-25m/"
movies = pd.read_csv(data_path + "movies.csv")
ratings = pd.read_csv(data_path + "usable_ratings.csv")
genome_tags = pd.read_csv(data_path + "genome-tags.csv")
genome_scores = pd.read_csv(data_path + "genome-scores.csv")
genome_scores = pd.merge(genome_scores, genome_tags, on='tagId', how='inner')

print(f"# Movies = {ratings['movieId'].nunique()}")
print(f"# Users = {ratings['userId'].nunique()}")
print(f"# Ratings = {len(ratings)}")
print(f"# Tags = {len(genome_tags)}")

# %% [markdown]
# ## Set avg rating column for each movie in movies DF

# %%
# mean is about all users including those who did't vote for that movie
gr_movie_ratings = ratings.groupby(by="movieId")
no_users = ratings['userId'].nunique()
mean_rating_df = pd.DataFrame([], columns=["movieId", "meanRating"])
tmp_data = [[], []]

for name, group in gr_movie_ratings:
    mean_rating = group["rating"].sum() / no_users
    tmp_data[0].append(name)
    tmp_data[1].append(mean_rating)

mean_rating_df["movieId"] = tmp_data[0]
mean_rating_df["meanRating"] = tmp_data[1]

movies = pd.merge(movies, mean_rating_df, on="movieId", how="left")

# %% [markdown]
# ## Extract base movie categories

# %%
categs_col_strs = list(movies["genres"])
categs_col_strs = [categ_str.split("|") for categ_str in categs_col_strs]
base_categs_list = []
for categs_str in categs_col_strs:
    base_categs_list += categs_str


base_categs_list = list(set(base_categs_list))
base_categs_list.remove("(no genres listed)")
base_categs_list.sort()
base_categs_list = [categ.lower() for categ in base_categs_list]

del categs_col_strs

print("Number of usable categories = ", len(base_categs_list))

# %%
# base_categs_list

# %% [markdown]
# ## Prepare data for KNN the classifier

# %%
# piv_matrix = valid_ratings.pivot(index="movieId", columns="userId", values="rating")
piv_matrix = ratings.pivot(index="userId", columns="movieId", values="rating")
piv_matrix.fillna(0, inplace=True)

# %%
# fill NaN's with the mean

# for col in list(piv_matrix.columns):
#     mean = piv_matrix[col].mean()
#     piv_matrix[col].fillna(mean, inplace=True)

# %%
csr_data = csr_matrix(piv_matrix)
csr_data = csr_data.transpose()  # ! issue in col and row

# %%
knn = NearestNeighbors(metric='cosine', algorithm='brute',
                       n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)

# %% [markdown]
# # Recommendation

# %%


def get_movie_id(movie_name):
    try:
        ids = movies[movies['title'].str.lower().str.contains(
            movie_name.lower().strip())]["movieId"].values
        return ids
    except:
        # if does not exist reutrn []
        print("ERR")
        return []

# %% [markdown]
# ## Rating Recommendation : Based similar ratings by all users (similar combination of ratings)

# %%


def recommend_based_on_similar_ratings(movie_id, no_of_similars=5):
    # assumes a valid movie_id : int

    recommended_movies = []
    recommended_movies_with_dist = []
    list_of_columns = list(piv_matrix.columns)

    try:
        movie_index = list_of_columns.index(movie_id)
        distances, indices = knn.kneighbors(
            csr_data[movie_index], n_neighbors=no_of_similars + 1)
        tmp = zip(list(distances[0]), list(indices[0]))

        for item in tmp:
            recommended_movies_with_dist.append(item)

    except:
        # failed to find a movie
        # print("failed to find a movie")
        pass

    recommended_movies_with_dist = sorted(
        list(set(recommended_movies_with_dist)))

    for item in recommended_movies_with_dist:
        movie_idx = item[1]
        new_movie_id = list_of_columns[movie_idx]

        if new_movie_id == movie_id:
            continue

        recommended_movie_name = movies[movies["movieId"]
                                        == new_movie_id]["title"].values[0]
        recommended_movies.append(
            {"id": new_movie_id, "name": recommended_movie_name})

    return recommended_movies

# %% [markdown]
# ## Identify top categories of a movie

# %%


def get_top_categs_of_movie(movie_id, top_k=5, is_dynamic_k=False):
    # assumes a valid movie_id : int
    # dynamic is for using a threshold for relevance not the static k
    # returns df(tag_id, tag, relevance)

    relevance_thr = 0.6  # used only in case of is_dynamic_k

    categs_sorted_by_relevance = genome_scores[genome_scores["movieId"] == movie_id].sort_values(
        by=['relevance'], ascending=False)[["tagId", "tag", "relevance"]]

    # base_categs = categs_sorted_by_relevance[categs_sorted_by_relevance["tag"].str.capitalize().isin(base_categs_list)]
    base_categs = categs_sorted_by_relevance[categs_sorted_by_relevance["tag"].isin(
        base_categs_list)]

    if is_dynamic_k == True:
        return base_categs[base_categs["relevance"] >= relevance_thr]
    else:
        top_k_categs = base_categs.iloc[:top_k]
        return top_k_categs

# %% [markdown]
# ## Category Recommendation : Based similar categories

# %%


def recommend_based_on_similar_categs(movie_id, top_k=5, is_dynamic_k=False, relevance_per_categ=0.8, min_mean_rating=2.5, k_movies_per_categ=3, sorting_order=["meanRating", "relevance"]):
    # assumes a valid movie_id : int
    # return { categ1: [], categ2: [], .... }

    recommendations = {}

    top_categs = list(get_top_categs_of_movie(
        movie_id, top_k=top_k, is_dynamic_k=is_dynamic_k)["tag"])

    # make a DF with movies within each top_categs, each movie has relevance >= relevance_per_categ
    # sorted by the rating and relevance
    valid_movies_categ_relevanve_rating_name = genome_scores[(genome_scores["tag"].isin(
        top_categs)) & (genome_scores["relevance"] >= relevance_per_categ)]
    valid_movies_categ_relevanve_rating_name = pd.merge(
        valid_movies_categ_relevanve_rating_name, movies[["movieId", "title", "meanRating"]], on="movieId")

    valid_movies_categ_relevanve_rating_name = valid_movies_categ_relevanve_rating_name.sort_values(
        by=sorting_order, ascending=False)

    # fetching and fill k_movies_per_categ
    gr_valid_movies = valid_movies_categ_relevanve_rating_name.groupby(
        by="tag")

    for tag, group in gr_valid_movies:
        current_movies = []

        for movie in group[:k_movies_per_categ][["movieId", "title"]].values:
            current_movies.append({"id": movie[0], "name": movie[1]})
        recommendations[tag] = current_movies

    return recommendations

# %%
# tmp = recommend_based_on_similar_categs(2, is_dynamic_k=False, relevance_per_categ=0.9)
# print(tmp)
# for key in tmp:
#     print("\n==== ",key," ====\n", tmp[key])

# %% [markdown]
# ## General Recommendation : Based on similar ratings and similar categories

# %%


def general_recommendation(movie_id):
    # assumes a valid movie_id : int
    # * return { similar_movies: [], based_on_categs: { categ1: [], categ2: [], .... } }

    similar_movies = recommend_based_on_similar_ratings(movie_id)
    recommend_based_on_categs = recommend_based_on_similar_categs(movie_id)

    return {"similar_movies": similar_movies, "based_on_categs": recommend_based_on_categs}

# %%
# general_recommendation(1)

# %% [markdown]
# ## Given set of categories, recommend!

# %%
# recommend movies based on one categ


def get_movies_df_in_categ(categ, min_categ_relevance=0.5, min_mean_rating=2.5):
    good_movies_with_rating_categ = movies[(movies["genres"].str.lower().str.find(categ.lower()) > -1) &
                                           (movies["meanRating"] >= min_mean_rating)]

    good_scores = genome_scores[(genome_scores["relevance"] >= min_categ_relevance) &
                                (genome_scores["tag"] == categ.lower()) &
                                (genome_scores["movieId"].isin(list(good_movies_with_rating_categ["movieId"])))]

    ret = pd.merge(good_movies_with_rating_categ[["movieId", "title", "meanRating"]], good_scores[[
                   "movieId", "relevance", "tag"]], on="movieId", how="inner")
    return ret

# %%
# recommend movies based on a set of categ


def recommend_given_categories(categs, min_categ_relevances=[], default_relevance=0.5, top_k=15):
    # returns top_k movies with a combination of categories with relevances to each categ and sorted by rating
    # @ categs : categs from " base_categs_list "
    # @ min_categ_relevances : minimum relevance for each categ, default is [ default_relevance, default_relevance, default_relevance, .... ]

    while len(min_categ_relevances) < len(categs):
        min_categ_relevances.append(default_relevance)

    good_relevance_ids = []
    gr_movies = genome_scores[genome_scores["tag"].str.lower().isin(categs) &
                              (genome_scores["relevance"]
                               >= min(min_categ_relevances))
                              ].groupby(by="movieId")

    for movie_id, group in gr_movies:
        is_good_movie = True
        for idx in range(len(categs)):
            categ = categs[idx]
            relev = min_categ_relevances[idx]
            if len(group.query(f"tag == '{categ}' and relevance >= {relev}")) == 0:
                is_good_movie = False
                break

        if is_good_movie == True:
            good_relevance_ids.append(movie_id)

    selected_movies = movies[movies["movieId"].isin(good_relevance_ids)]\
        .sort_values(by=["meanRating"], ascending=False)[:top_k]
    return selected_movies


# %%
recommend_given_categories(["musical", "children"], default_relevance=0.7)
# lengenome_scores.query(f"tag == '{'action'}' and relevance >= {0.9}")

# %% [markdown]
# ## Given a user state, recommend!

# %%
# #TODO liked list movies by our user
# liked_movie_names = ["Toy story", "lion king"]

# %% [markdown]
# ## Test

# %%
movie_name = "Toy story"
recommendations = general_recommendation(get_movie_id("Toy story")[0])

print(f"======= Movie: {movie_name} =======\n")
print("Similar movies based on ratings")
for movie in recommendations["similar_movies"]:
    print(movie)
print("-------------------------------")

print("Based on categories")
for category in recommendations["based_on_categs"]:
    print(category)
    for movie in recommendations["based_on_categs"][category]:
        print(movie)
    # print("-------------------------------")

# %%


class movie_recommender:
    def __init__(self) -> None:
        self.movies = movies
        self.piv_matrix = piv_matrix
        self.knn = knn
        self.csr_data = csr_data
        self.genome_scores = genome_scores
        self.base_categs_list = base_categs_list
        self.pd = pd
        pass

    def get_movie_id(self, movie_name):
        try:
            ids = self.movies[self.movies['title'].str.lower().str.contains(
                movie_name.lower().strip())]["movieId"].values
            return ids
        except:
            return []

    def recommend_based_on_similar_ratings(self, movie_id, no_of_similars=5):
        recommended_movies = []
        recommended_movies_with_dist = []
        list_of_columns = list(self.piv_matrix.columns)

        try:
            movie_index = list_of_columns.index(movie_id)
            distances, indices = self.knn.kneighbors(
                self.csr_data[movie_index], n_neighbors=no_of_similars + 1)
            tmp = zip(list(distances[0]), list(indices[0]))

            for item in tmp:
                recommended_movies_with_dist.append(item)
        except:
            pass

        recommended_movies_with_dist = sorted(
            list(set(recommended_movies_with_dist)))

        for item in recommended_movies_with_dist:
            movie_idx = item[1]
            new_movie_id = list_of_columns[movie_idx]

            if new_movie_id == movie_id:
                continue

            recommended_movie_name = self.movies[self.movies["movieId"]
                                                 == new_movie_id]["title"].values[0]
            recommended_movies.append(
                {"id": new_movie_id, "name": recommended_movie_name})

        return recommended_movies

    def get_top_categs_of_movie(self, movie_id, top_k=5, is_dynamic_k=False):
        relevance_thr = 0.6

        categs_sorted_by_relevance = self.genome_scores[self.genome_scores["movieId"] == movie_id].sort_values(
            by=['relevance'], ascending=False)[["tagId", "tag", "relevance"]]

        base_categs = categs_sorted_by_relevance[categs_sorted_by_relevance["tag"].isin(
            self.base_categs_list)]

        if is_dynamic_k == True:
            return base_categs[base_categs["relevance"] >= relevance_thr]

        else:
            top_k_categs = base_categs.iloc[:top_k]
            return top_k_categs

    def recommend_based_on_similar_categs(self, movie_id, top_k=5, is_dynamic_k=True, relevance_per_categ=0.8, min_mean_rating=2.5, k_movies_per_categ=3, sorting_order=["meanRating", "relevance"]):

        recommendations = {}
        top_categs = list(self.get_top_categs_of_movie(
            movie_id, top_k=top_k, is_dynamic_k=is_dynamic_k)["tag"])

        valid_movies_categ_relevanve_rating_name = self.genome_scores[(self.genome_scores["tag"].isin(
            top_categs)) & (self.genome_scores["relevance"] >= relevance_per_categ)]
        valid_movies_categ_relevanve_rating_name = self.pd.merge(
            valid_movies_categ_relevanve_rating_name, self.movies[["movieId", "title", "meanRating"]], on="movieId")

        valid_movies_categ_relevanve_rating_name = valid_movies_categ_relevanve_rating_name.sort_values(
            by=sorting_order, ascending=False)

        # fetching and fill k_movies_per_categ
        gr_valid_movies = valid_movies_categ_relevanve_rating_name.groupby(
            by="tag")

        for tag, group in gr_valid_movies:
            current_movies = []

            for movie in group[:k_movies_per_categ][["movieId", "title"]].values:
                current_movies.append({"id": movie[0], "name": movie[1]})
            recommendations[tag] = current_movies

        return recommendations

    def general_recommendation(self, movie_id):
        similar_movies = self.recommend_based_on_similar_ratings(movie_id)
        recommend_based_on_categs = self.recommend_based_on_similar_categs(
            movie_id)

        return {"similar_movies": similar_movies, "based_on_categs": recommend_based_on_categs}

    def recommend_given_categories(self, categs, min_categ_relevances=[], default_relevance=0.5, top_k=15):
        while len(min_categ_relevances) < len(categs):
            min_categ_relevances.append(default_relevance)

        good_relevance_ids = []
        gr_movies = self.genome_scores[self.genome_scores["tag"].str.lower().isin(categs) &
                                       (self.genome_scores["relevance"] >= min(
                                           min_categ_relevances))
                                       ].groupby(by="movieId")

        for movie_id, group in gr_movies:
            is_good_movie = True
            for idx in range(len(categs)):
                categ = categs[idx]
                relev = min_categ_relevances[idx]
                if len(group.query(f"tag == '{categ}' and relevance >= {relev}")) == 0:
                    is_good_movie = False
                    break

            if is_good_movie == True:
                good_relevance_ids.append(movie_id)

        selected_movies = self.movies[self.movies["movieId"].isin(good_relevance_ids)]\
            .sort_values(by=["meanRating"], ascending=False)[:top_k]
        return selected_movies


# %%
model = movie_recommender()
# model.recommend_given_categories(["musical", "children"], default_relevance=0.7)

# %%

path = "../utils/movie_recommender"

with open(path, 'wb') as f:
    pickle.dump(model, f)
