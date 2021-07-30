import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_similar_movies(liked_movies):
    data = pd.read_csv("content/movies_metadata.csv")
    count = CountVectorizer(stop_words='english')
    indices = pd.Series(data.index, index=data['title'])
    count_matrix = count.fit_transform(data['combined'].astype('U'))
    global_sim_scores = []
    for movie_title in liked_movies:
        idx = indices[movie_title]
        cosine_sim = cosine_similarity(count_matrix[idx], count_matrix)
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        global_sim_scores.extend(sim_scores)
    global_sim_scores = sorted(global_sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in global_sim_scores]
    return list(data.iloc[movie_indices]['title'])


def get_recommendation(rated_movies, liked_movies):
    similar_movies = get_similar_movies(liked_movies)
    recommended_movies = [movie for movie in similar_movies if movie not in rated_movies]
    recommended_movies = list(set(recommended_movies))
    if len(recommended_movies) > 30:
        recommended_movies = recommended_movies[0:30]
    return recommended_movies
