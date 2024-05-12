import streamlit as st
import pandas as pd
import pickle
import requests
from requests.exceptions import Timeout, RequestException
from PIL import Image

# Function to fetch movie poster with robust error handling
def fetch_poster(movie_id):
    api_key = "13f47a39b05529f6e82312c80039a0e9"  # Replace with your actual API key
    base_url = "https://api.themoviedb.org/3/movie/"
    image_base_url = "https://image.tmdb.org/t/p/w500"  # Poster size (w500 for medium)

    try:
        # Fetch movie details to get the poster path
        details_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(details_url, timeout=5)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return f"{image_base_url}{poster_path}"  # Return the full poster URL
        else:
            print(f"Poster not found for movie ID {movie_id}")  # Log a message if no poster
            return None
    
    except (Timeout, RequestException) as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return None

# Function to get movie description
def get_movie_description(movie_id):
    api_key = "13f47a39b05529f6e82312c80039a0e9"  # Replace with your API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data.get("overview", "Description not available")

# Load the datasets
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function (with caching and error handling)
@st.cache_data
def recommend(movie):
    # Load the datasets
    movies = pickle.load(open('movies.pkl','rb'))  # Move this line up
    similarity = pickle.load(open('similarity.pkl', 'rb')) # Move this line up
    if movie not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    for i, _ in movies_list:
        movie_id = movies.iloc[i].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movies.append(movies.iloc[i]['title'])
            recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

# ... your code for loading datasets movies and similarity

# Streamlit App
st.title('Movie Recommendation App')

selected_movie = st.selectbox('Select a movie to get recommendations', movies['title'].values)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie)
    num_recommendations = len(names)

    # CSS styling (unchanged)

    # Display posters with descriptions
    st.markdown('<div class="poster-grid">', unsafe_allow_html=True)
    for index, (name, poster) in enumerate(zip(names, posters)):  # Using enumerate
        if poster:
            st.markdown(f'''
            <div class="poster">
                <img src="{poster}" style="width: 100%; height: auto;">
                <p style="text-align: center;">{name}</p>
                <p style="text-align: center;">{get_movie_description(movies.iloc[index].movie_id)}</p>
            </div>
            ''', unsafe_allow_html=True) 
    st.markdown('</div>', unsafe_allow_html=True)
