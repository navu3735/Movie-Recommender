import streamlit as st 
import pickle 
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0dc630884cea0d7db05826e7bcfe25d7&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return 'http://image.tmdb.org/t/p/w500/' + poster_path
    return 'https://via.placeholder.com/500x750?text=No+Poster+Available'

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_sorted:
        # Adjust this line based on your actual movie ID column name
        movie_id = movies_df.iloc[i[0]]['movie_id']  # Replace 'movie_id' with your actual column name
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_movies_posters

# Load the movies DataFrame and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movies_df['title'].values

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie:",
    movie_titles
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])