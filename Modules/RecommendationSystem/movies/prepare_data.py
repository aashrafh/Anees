#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


# In[2]:


data_path = "../Data/ml-25m/"
movies = pd.read_csv(data_path + "movies.csv")
ratings = pd.read_csv(data_path + "ratings.csv")
print(f"# Movies = {ratings['movieId'].nunique()}")
print(f"# Users = {ratings['userId'].nunique()}")
print(f"# Ratings = {len(ratings)}")


# In[3]:


no_users_voted_to_a_movie = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted_by_a_user = ratings.groupby('userId')['rating'].agg('count')


# In[4]:


# user_votes_thr = 350
# movie_votes_thr = 1500

user_votes_thr = 400
movie_votes_thr = 1800


# In[5]:


# Number of movies are voted by each user (e.g. user activity and reliability)
f,ax = plt.subplots(1,1,figsize=(16,4))
plt.scatter(no_movies_voted_by_a_user.index,no_movies_voted_by_a_user,color='mediumseagreen')
plt.axhline(y=user_votes_thr,color='r')
plt.xlabel('UserId')
plt.ylabel('No. of moveis are voted to')
plt.show()


# In[6]:


# drop any user or movie with no. of votes less than the threshold
list_of_active_users_idx = list(no_movies_voted_by_a_user[no_movies_voted_by_a_user >= user_votes_thr].index)
list_of_popular_movies_idx = list(no_users_voted_to_a_movie[no_users_voted_to_a_movie >= movie_votes_thr].index)
valid_ratings = ratings.query(f"userId in {list_of_active_users_idx} and movieId in {list_of_popular_movies_idx}")


# In[7]:


print(f"# Movies = {valid_ratings['movieId'].nunique()}")
print(f"# Users = {valid_ratings['userId'].nunique()}")
print(f"# Ratings = {len(valid_ratings)}")


# In[8]:


valid_ratings.to_csv(data_path + "usable_ratings.csv", encoding='utf-8', index=False)

