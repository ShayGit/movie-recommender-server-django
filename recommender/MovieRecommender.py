import numpy as np
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_similar_movies(title):
    data = pd.read_csv("content/movies_metadata.csv")
    count = CountVectorizer(stop_words='english')
    indices = pd.Series(data.index, index=data['title'])
    count_matrix = count.fit_transform(data['combined'].astype('U'))
    idx = indices[title]
    cosine_sim = cosine_similarity(count_matrix[idx], count_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return list(data.iloc[movie_indices]['title'])


def check_seen(recommended_movie, rated_movies):
    for index, movie in enumerate(rated_movies):
        if recommended_movie == movie.title:
            return True
    return False


def get_recommendation(rated_movies, liked_movies):
    similar_movies = []
    for index, movie in enumerate(liked_movies):
        similar_movies.extend(get_similar_movies(movie.title))

    similar_movies.sort()

    recommended_movies = []
    for movie_title in similar_movies:
        if not check_seen(movie_title, rated_movies):
            recommended_movies.append(movie_title)

    if len(recommended_movies) > 30:
        recommended_movies = recommended_movies[0:30]

    return recommended_movies
