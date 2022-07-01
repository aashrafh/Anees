#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# In[ ]:

print("Reading data")
data_path = "../Data/ml-25m/"
movies = pd.read_csv(data_path + "movies.csv")
ratings = pd.read_csv(data_path + "usable_ratings.csv")
print(f"# Movies = {ratings['movieId'].nunique()}")
print(f"# Users = {ratings['userId'].nunique()}")
print(f"# Ratings = {len(ratings)}")


# In[ ]:

print("Creating pivot")
# piv_matrix = valid_ratings.pivot(index="movieId", columns="userId", values="rating")
piv_matrix = ratings.pivot(index="userId", columns="movieId", values="rating")
piv_matrix.fillna(0, inplace=True)


# In[ ]:


# fill NaN's with the mean

# print("filling NaN")
# for col in list(piv_matrix.columns):
#     mean = piv_matrix[col].mean()
#     piv_matrix[col].fillna(mean, inplace=True)


# In[ ]:


print("Creating csr_matrix")
csr_data = csr_matrix(piv_matrix)
csr_data = csr_data.transpose() #! issue in col and row


# In[ ]:

print("Training the model")
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)

# In[ ]:


def get_movie_id(movie_name):
    try:
        ids = movies[movies['title'].str.lower().str.contains(movie_name.lower())]["movieId"].values
        return ids
    except:
        # if does not exist reutrn []
        return []

def get_similar_movies(movie_name, no_of_similars = 5):
    ids = get_movie_id(movie_name)
    if len(ids) == 0:
        # if does not exist reutrn []
        return []

    recommended_movies = []
    recommended_movies_with_dist = []
    list_of_columns = list(piv_matrix.columns)
	
    
    for id in ids:
        try:
            movie_index = list_of_columns.index(id)
            distances , indices = knn.kneighbors(csr_data[movie_index],n_neighbors= no_of_similars + 1)
            tmp = zip(list(distances[0]), list(indices[0]))

            for item in tmp:
                recommended_movies_with_dist.append(item)
            
        except:
            # failed to find a movie
            print("failed to find a movie")
            pass
            
    recommended_movies_with_dist = sorted(list(set(recommended_movies_with_dist)))

    for item in recommended_movies_with_dist:
        movie_idx = item[1]
        movie_id = list_of_columns[movie_idx]
        recommended_movie_name = movies[movies["movieId"] == movie_id]["title"].values[0]
        recommended_movies.append(recommended_movie_name)

    return recommended_movies

while True:
    x, k = str(input("Movie name:  \n")), int(input("K:  \n"))
    if len(x) == 0 or x == "": continue
    similars = get_similar_movies(x, k)
    print(similars)
    print("---------------------")


# ## Given a user state, recommend!

# In[ ]:


# liked list movies by our user
liked_movies = ["Toy story", "lion king"]

print("DONEEEE!!!!")


# In[ ]:




